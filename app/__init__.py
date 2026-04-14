from datetime import datetime
from flask import Flask, jsonify
import os
import logging
from pymongo import ASCENDING

# Import your custom exceptions and extensions
from app.exception.copy_exception import CopyException
from app.exception.email_delivery_exception import EmailDeliveryException
from .extensions import mongo
from dotenv import load_dotenv

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Load .env only for local development (Render uses environment variables)
    if os.getenv("FLASK_ENV") != "production":
        load_dotenv()
    
    # MongoDB URI
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        logger.error("MONGO_URI environment variable is not set!")
        raise RuntimeError("MONGO_URI environment variable is not set!")

    app.config["MONGO_URI"] = mongo_uri
    app.config["MONGO_MAX_POOL_SIZE"] = int(os.getenv("MONGO_MAX_POOL_SIZE", 100))

    # Initialize mongo with lazy connection (safer with Gunicorn)
    try:
        mongo.init_app(app)
        
        # Test connection inside app context
        with app.app_context():
            mongo.cx.admin.command('ping')
            logger.info("✅ Successfully connected to MongoDB Atlas!")
            
    except Exception as e:
        logger.error(f"❌ MongoDB Connection Failed: {str(e)}")
        # Do NOT raise here during production if you want the app to start
        # (but keep it for now so you see the exact error in Render logs)
        raise

    # TTL Index Creation (safe, won't crash startup)
    try:
        with app.app_context():
            if 'otp_verifications' in mongo.db.list_collection_names():
                indexes = mongo.db.otp_verifications.index_information()
                if 'expires_at_1' not in indexes:
                    mongo.db.otp_verifications.create_index(
                        [("expires_at", ASCENDING)],
                        expireAfterSeconds=0
                    )
                    logger.info("✅ TTL index created on otp_verifications.expires_at")
                else:
                    logger.info("TTL index already exists")
            else:
                logger.info("otp_verifications collection does not exist yet. TTL index will be created on first use.")
    except Exception as e:
        logger.warning(f"Could not create TTL index: {e}")

    # Register routes
    from .routes import register_routes
    register_routes(app)

    return app