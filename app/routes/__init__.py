from .authentication import auth_bp
from .otp_verification import email_verification_bp
from .cloudinary import cloudinary_bp
from .auth_routes import token_bp
from .agent_routes import agent_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(email_verification_bp)
    app.register_blueprint(cloudinary_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(agent_bp)

