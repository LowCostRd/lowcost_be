from datetime import datetime


from flask import Flask, jsonify
from app.exception.copy_exception import CopyException
from app.exception.email_delivery_exception import EmailDeliveryException
from .extensions import mongo
from dotenv import load_dotenv
import os
import logging
from pymongo import ASCENDING  

def create_app():
    app = Flask(__name__)
    logger = logging.getLogger(__name__)
    load_dotenv()
  
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["MONGO_POOL_SIZE"] = os.getenv("MONGO_POOL_SIZE")
    app.config["MONGO_MAX_POOL_SIZE"] = os.getenv("MONGO_MAX_POOL_SIZE")

    mongo.init_app(app)

    # === TTL index creation ===
    with app.app_context():
        indexes = mongo.db.otp_verifications.index_information()
        if 'expires_at_1' not in indexes:
            mongo.db.otp_verifications.create_index(
                [("expires_at", ASCENDING)],
                expireAfterSeconds=0
            )
            print("TTL index created on otp_verifications.expires_at")

    from .routes import register_routes
    register_routes(app)

    @app.errorhandler(CopyException)
    def handle_copy_exception(error):
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(EmailDeliveryException)
    def handle_email_delivery_exception(error):
      return jsonify(error.to_dict()), 201 

    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred. Please try again later.",
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }), 500
    

    return app

    
