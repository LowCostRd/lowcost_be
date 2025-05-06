from .authentication import auth_bp
from .otp_verification import email_verification_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(email_verification_bp)
