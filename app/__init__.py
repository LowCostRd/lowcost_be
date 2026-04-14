from datetime import datetime
from flask import Flask, jsonify
from app.exception.copy_exception import CopyException
from app.exception.email_delivery_exception import EmailDeliveryException
from .extensions import mongo
from dotenv import load_dotenv
import os
import logging
from pymongo import ASCENDING  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Load env vars (safe for both local and Render)
    load_dotenv()  
    
    # Critical: Use Render's $PORT, fallback for local
    port = int(os.getenv("PORT", 5000))
    
    # Mongo config
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI environment variable is not set!")
    
    app.config["MONGO_URI"] = mongo_uri
    app.config["MONGO_POOL_SIZE"] = int(os.getenv("MONGO_POOL_SIZE", 100))
    app.config["MONGO_MAX_POOL_SIZE"] = int(os.getenv("MONGO_MAX_POOL_SIZE", 100))

    mongo.init_app(app)

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

    # TTL index (move inside try/except to avoid startup crash)
    try:
        with app.app_context():
            indexes = mongo.db.otp_verifications.index_information()
            if 'expires_at_1' not in indexes:
                mongo.db.otp_verifications.create_index(
                    [("expires_at", ASCENDING)],
                    expireAfterSeconds=0
                )
                print(" TTL index created on otp_verifications.expires_at")
    except Exception as e:
        print(f" Could not create TTL index (maybe collection doesn't exist yet): {e}")

    # Register routes
    from .routes import register_routes
    register_routes(app)

    return app