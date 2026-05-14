from functools import wraps
from flask import request, jsonify, g
from datetime import datetime
import jwt
import logging
 
from .token_service import decode_access_token
logger = logging.getLogger(__name__)
 
 
def _extract_bearer() -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None
 
 
def _unauthorized(message: str, code: int = 401):
    return jsonify({
        "success":       False,
        "error_message": message,
        "status_code":   code,
        "time_stamp":    datetime.now().isoformat(),
    }), code
 
 
# ── require_auth ──────────────────────────────────────────────────────────────
 
def require_auth(f):
    """Validates the JWT access token and injects g.current_user."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_bearer()
        if not token:
            return _unauthorized("Missing or malformed Authorization header.")
        try:
            payload = decode_access_token(token)
        except jwt.ExpiredSignatureError:
            return _unauthorized("Access token has expired.")
        except jwt.InvalidTokenError as e:
            return _unauthorized(f"Invalid token: {str(e)}")
        except Exception:
            logger.exception("Unexpected error during token decode.")
            return _unauthorized("Token validation failed.", 500)
 
        g.current_user = {
            "sub":   payload["sub"],
            "email": payload["email"],
            "roles": payload.get("roles", []),
            "jti":   payload["jti"],
            "exp":   payload["exp"],
        }
        return f(*args, **kwargs)
    return decorated
 
 
# ── require_roles ─────────────────────────────────────────────────────────────
 
def require_roles(*required_roles: str):
    """
    Role-based access control. Must be used AFTER @require_auth.
 
    Example:
        @bp.route("/admin")
        @require_auth
        @require_roles("admin")
        def admin_only(): ...
 
        @bp.route("/mod")
        @require_auth
        @require_roles("admin", "moderator")   # any of these roles is sufficient
        def mod_panel(): ...
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if user is None:
                return _unauthorized("Authentication required.")
            user_roles = set(user.get("roles", []))
            if not user_roles.intersection(required_roles):
                return _unauthorized(
                    f"Access denied. Required role(s): {', '.join(required_roles)}",
                    403,
                )
            return f(*args, **kwargs)
        return decorated
    return decorator
 
 
# ── optional_auth ─────────────────────────────────────────────────────────────
 
def optional_auth(f):
    """
    Tries to authenticate but never rejects the request.
    g.current_user will be None if no valid token is provided.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_bearer()
        g.current_user = None
        if token:
            try:
                payload = decode_access_token(token)
                g.current_user = {
                    "sub":   payload["sub"],
                    "email": payload["email"],
                    "roles": payload.get("roles", []),
                    "jti":   payload["jti"],
                }
            except Exception:
                pass  # Silently ignore — route handles anonymous users
        return f(*args, **kwargs)
    return decorated
 