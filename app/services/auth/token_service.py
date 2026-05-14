from datetime import datetime, timezone, timedelta
from typing import Optional
import jwt
import os
import uuid
import logging
 
from app.extensions import mongo
from dotenv import load_dotenv
load_dotenv()
 
logger = logging.getLogger(__name__)
 
# ── Config ────────────────────────────────────────────────────────────────────
 
ACCESS_SECRET  = os.getenv("JWT_ACCESS_SECRET")
REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")
 
ACCESS_TTL_MINUTES  = int(os.getenv("ACCESS_TOKEN_TTL_MINUTES",  15))
REFRESH_TTL_DAYS    = int(os.getenv("REFRESH_TOKEN_TTL_DAYS",     7))
 
ALGORITHM = os.getenv("ALGORITHM_CODE")

 
 
def _require_secrets() -> None:
    if not ACCESS_SECRET or not REFRESH_SECRET:
        raise RuntimeError(
            "JWT_ACCESS_SECRET and JWT_REFRESH_SECRET must be set in environment."
        )
 
 
# ── Token Creation ────────────────────────────────────────────────────────────
 
def create_access_token(user_id: str, email: str, roles: list[str]) -> str:
    _require_secrets()
    now = datetime.now(timezone.utc)
    payload = {
        "sub":   str(user_id),
        "email": email,
        "roles": roles,
        "type":  "access",
        "iat":   now,
        "exp":   now + timedelta(minutes=ACCESS_TTL_MINUTES),
        "jti":   str(uuid.uuid4()),
    }
    return jwt.encode(payload, ACCESS_SECRET, algorithm=ALGORITHM)
 
 
def create_refresh_token(user_id: str) -> str:
    _require_secrets()
    now = datetime.now(timezone.utc)
    payload = {
        "sub":  str(user_id),
        "type": "refresh",
        "iat":  now,
        "exp":  now + timedelta(days=REFRESH_TTL_DAYS),
        "jti":  str(uuid.uuid4()),
    }
    return jwt.encode(payload, REFRESH_SECRET, algorithm=ALGORITHM)
 
 
# ── Token Verification ────────────────────────────────────────────────────────
 
def decode_access_token(token: str) -> dict:
    """
    Returns decoded payload or raises jwt.PyJWTError subclasses.
    Caller is responsible for catching and returning 401.
    """
    _require_secrets()
    payload = jwt.decode(token, ACCESS_SECRET, algorithms=[ALGORITHM])
    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Not an access token.")
    if is_blacklisted(payload["jti"]):
        raise jwt.InvalidTokenError("Token has been revoked.")
    return payload
 
 
def decode_refresh_token(token: str) -> dict:
    _require_secrets()
    payload = jwt.decode(token, REFRESH_SECRET, algorithms=[ALGORITHM])
    if payload.get("type") != "refresh":
        raise jwt.InvalidTokenError("Not a refresh token.")
    if is_blacklisted(payload["jti"]):
        raise jwt.InvalidTokenError("Refresh token has been revoked.")
    return payload
 
 
# ── Blacklist (MongoDB TTL) ───────────────────────────────────────────────────
 
def blacklist_token(jti: str, expires_at: datetime) -> None:
    """Persist a JTI to the blacklist until its natural expiry."""
    try:
        mongo.db.token_blacklist.insert_one({
            "jti":        jti,
            "expires_at": expires_at,          # TTL index fires here
            "created_at": datetime.now(timezone.utc),
        })
    except Exception:
        logger.exception("Failed to blacklist token jti=%s", jti)
        raise
 
 
def is_blacklisted(jti: str) -> bool:
    return mongo.db.token_blacklist.find_one({"jti": jti}) is not None
 
 
def ensure_blacklist_ttl_index() -> None:
    """Call once at app startup (inside app context)."""
    indexes = mongo.db.token_blacklist.index_information()
    if "expires_at_1" not in indexes:
        from pymongo import ASCENDING
        mongo.db.token_blacklist.create_index(
            [("expires_at", ASCENDING)],
            expireAfterSeconds=0,
            name="expires_at_1",
        )
        logger.info("✅ TTL index created on token_blacklist.expires_at")
 