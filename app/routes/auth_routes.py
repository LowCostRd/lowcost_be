from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, make_response, g
import bcrypt
import jwt
import logging
import os
from app.extensions import mongo
from ..services.auth.token_service import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    decode_access_token,
    blacklist_token,
    ACCESS_TTL_MINUTES,
    REFRESH_TTL_DAYS,
)
from ..services.auth.decorators import require_auth
from ..services.rate_limiter import limiter
 
logger = logging.getLogger(__name__)
 
token_bp = Blueprint("token", __name__, url_prefix="/auth")
 
REFRESH_COOKIE_NAME = os.getenv("REFRESH_COOKIE_NAME")
COOKIE_SECURE       = os.getenv("FLASK_ENV")
COOKIE_SAMESITE     = os.getenv("COOKIE_SAMESITE")
 
 
 
def _set_refresh_cookie(response, token: str) -> None:
    response.set_cookie(
        REFRESH_COOKIE_NAME,
        token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=int(timedelta(days=REFRESH_TTL_DAYS).total_seconds()),
        path="/auth",        
    )
 
 
def _clear_refresh_cookie(response) -> None:
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/auth")
 
 
def _error(message: str, code: int):
    return jsonify({
        "success":       False,
        "error_message": message,
        "status_code":   code,
        "time_stamp":    datetime.now().isoformat(),
    }), code
 
 
def _success(data: dict, code: int = 200):
    return jsonify({"success": True, "status_code": code, **data}), code
 
 

@token_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute; 50 per hour")  
def login():
    body = request.get_json(silent=True) or {}
    email    = (body.get("email") or "").strip().lower()
    password =  body.get("password") or "" 
 
    if not email or not password:
        return _error("Email and password are required.", 400)
 

    user = mongo.db.users.find_one({"email_address": email})

    if not user:
        return _error("Invalid email or password.", 401)
 
    if not user.get("is_active", True):
        return _error("Account is deactivated. Please contact support.", 403)
 
    if not user.get("is_verified", False): 
        return _error("Please verify your email before logging in.", 403)
 

    stored_hash = user.get("password", "").encode() 
    if not bcrypt.checkpw(password.encode(), stored_hash):
     
        mongo.db.users.update_one(
            {"_id": user["_id"]},
            {
                "$inc": {"failed_login_attempts": 1},
                "$set": {"last_failed_login": datetime.now(timezone.utc)},
            },
        )
        return _error("Invalid email or password.", 401)
 

    mongo.db.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "failed_login_attempts": 0,
                "last_login": datetime.now(timezone.utc),
            }
        },
    )
 
 
    user_id = str(user["_id"])
    roles   = user.get("roles", ["user"])
 
    access_token  = create_access_token(user_id, email, roles)
    refresh_token = create_refresh_token(user_id)
 

    _store_refresh_token(user_id, refresh_token)
 
    response = make_response(_success({
        "access_token":  access_token,
        "token_type":    "Bearer",
        "expires_in":    ACCESS_TTL_MINUTES * 60,
        "user": {
            "id":    user_id,
            "email": email,
            "roles": roles,
            "onboarding_step": user.get("onboarding_step", "verify-email"),
        },
    }, 200))
    _set_refresh_cookie(response, refresh_token)
    return response
 
 
 
@token_bp.route("/refresh", methods=["POST"])
@limiter.limit("30 per minute")
def refresh():
    old_refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not old_refresh_token:
        return _error("Refresh token not found.", 401)
 
    try:
        payload = decode_refresh_token(old_refresh_token)
    except jwt.ExpiredSignatureError:
        resp = make_response(_error("Refresh token has expired. Please log in again.", 401))
        _clear_refresh_cookie(resp)
        return resp
    except jwt.InvalidTokenError as e:
        resp = make_response(_error(f"Invalid refresh token: {str(e)}", 401))
        _clear_refresh_cookie(resp)
        return resp
 
    user_id = payload["sub"]
    old_jti = payload["jti"]
    old_exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
 
    stored = mongo.db.refresh_tokens.find_one({"jti": old_jti, "user_id": user_id})
    if not stored:
        
        logger.warning("Refresh token reuse detected for user_id=%s. Revoking all.", user_id)
        _revoke_all_refresh_tokens(user_id)
        resp = make_response(_error("Token reuse detected. All sessions have been invalidated.", 401))
        _clear_refresh_cookie(resp)
        return resp

    user = mongo.db.users.find_one({"_id": user_id})

    if not user or not user.get("is_active", True):
        return _error("User account not found or deactivated.", 403)

    blacklist_token(old_jti, old_exp)
    mongo.db.refresh_tokens.delete_one({"jti": old_jti})

    email = user["email_address"]
    roles = [user.get("role", "user")]

    new_access = create_access_token(user_id, email, roles)
    new_refresh = create_refresh_token(user_id)

    _store_refresh_token(user_id, new_refresh)
 
    response = make_response(_success({
        "access_token": new_access,
        "token_type":   "Bearer",
        "expires_in":   ACCESS_TTL_MINUTES * 60,
    }))
    _set_refresh_cookie(response, new_refresh)
    return response
 
 
 
@token_bp.route("/logout", methods=["POST"])
@require_auth
def logout():
    exp = datetime.fromtimestamp(g.current_user["exp"], tz=timezone.utc)
    blacklist_token(g.current_user["jti"], exp)
 

    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if refresh_token:
        try:
            payload = decode_refresh_token(refresh_token)
            refresh_exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            blacklist_token(payload["jti"], refresh_exp)
            mongo.db.refresh_tokens.delete_one({"jti": payload["jti"]})
        except Exception:
            pass  
 
    response = make_response(_success({"message": "Logged out successfully."}))
    _clear_refresh_cookie(response)
    return response
 
 
 
@token_bp.route("/logout-all", methods=["POST"])
@require_auth
def logout_all():
    """Invalidates ALL refresh tokens for this user (all devices)."""
    user_id = g.current_user["sub"]
 
    exp = datetime.fromtimestamp(g.current_user["exp"], tz=timezone.utc)
    blacklist_token(g.current_user["jti"], exp)
 
    _revoke_all_refresh_tokens(user_id)
 
    response = make_response(_success({"message": "Logged out from all devices."}))
    _clear_refresh_cookie(response)
    return response
 
 
@token_bp.route("/me", methods=["GET"])
@require_auth
def me():
    user = mongo.db.users.find_one(
        {"_id": g.current_user["sub"]}, 
        {"password": 0, "failed_login_attempts": 0},
    )
    if not user:
        return _error("User not found.", 404)

    user["_id"] = str(user["_id"])
    return _success({"user": user})
 
 
 
def _store_refresh_token(user_id: str, token: str) -> None:
    """Persist refresh token JTI so we can rotate and revoke-all."""
    payload = decode_refresh_token(token)
    mongo.db.refresh_tokens.insert_one({
        "jti":        payload["jti"],
        "user_id":    user_id,
        "expires_at": datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
        "created_at": datetime.now(timezone.utc),
    })
 
 
def _revoke_all_refresh_tokens(user_id: str) -> None:
    """Blacklists and deletes every active refresh token for a user."""
    tokens = list(mongo.db.refresh_tokens.find({"user_id": user_id}))
    for t in tokens:
        try:
            blacklist_token(t["jti"], t["expires_at"])
        except Exception:
            pass
    mongo.db.refresh_tokens.delete_many({"user_id": user_id})
    logger.info("Revoked %d refresh token(s) for user_id=%s", len(tokens), user_id)