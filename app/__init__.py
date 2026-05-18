from datetime import datetime
 
from flask import Flask, jsonify
from pymongo import ASCENDING
 
from app.exception.copy_exception import CopyException
from app.exception.email_delivery_exception import EmailDeliveryException
from .extensions import mongo

from .services.rate_limiter import limiter
from .services.auth.token_service import ensure_blacklist_ttl_index
 
from dotenv import load_dotenv
import os
import logging
from flask_cors import CORS
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
 
def create_app():
    app = Flask(__name__)
 
    load_dotenv()
 
   
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI environment variable is not set!")
 
    app.config["MONGO_URI"]          = mongo_uri
    app.config["MONGO_POOL_SIZE"]     = int(os.getenv("MONGO_POOL_SIZE",     100))
    app.config["MONGO_MAX_POOL_SIZE"] = int(os.getenv("MONGO_MAX_POOL_SIZE", 100))
 
  
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    CORS(
        app,
        origins=allowed_origins,
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    )
 

    mongo.init_app(app)
    limiter.init_app(app)
 

    try:
        with app.app_context():
            mongo.cx.admin.command("ping")
            logger.info("✅ Successfully connected to MongoDB Atlas!")
    except Exception as e:
        logger.error("❌ MongoDB Connection Failed: %s", str(e))
        raise
 

    _create_indexes(app)
 
    _register_error_handlers(app)
 
    from .routes import register_routes
    register_routes(app)

 
    return app

 
 
def _create_indexes(app: Flask) -> None:
    index_specs = [
        # collection, field, extra_kwargs
        ("otp_verifications", "expires_at",    {"expireAfterSeconds": 0}),
        ("token_blacklist",   "expires_at",    {"expireAfterSeconds": 0}),
        ("refresh_tokens",    "expires_at",    {"expireAfterSeconds": 0}),
        ("refresh_tokens",    "user_id",       {}),
        ("users",             "email_address",         {"unique": True}),

        ("agents",            "agent_id",      {"unique": True}), 
        ("agents",            "user_id",       {}),   
    ]
    with app.app_context():
        for collection_name, field, kwargs in index_specs:
            try:
                collection = mongo.db[collection_name]
                existing   = collection.index_information()
                index_name = f"{field}_1"
                if index_name not in existing:
                    collection.create_index([(field, ASCENDING)], name=index_name, **kwargs)
                    logger.info("✅ Index '%s' created on %s", index_name, collection_name)
            except Exception as e:
                logger.warning("⚠️  Could not create index '%s' on %s: %s", field, collection_name, e)
 
 
def _register_error_handlers(app: Flask) -> None:
 
    @app.errorhandler(CopyException)
    def handle_copy_exception(e: CopyException):
        return jsonify(e.to_dict()), e.code
 
    @app.errorhandler(EmailDeliveryException)
    def handle_email_delivery_exception(e: EmailDeliveryException):
        return jsonify(e.to_dict()), e.code
 
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "success":       False,
            "error_message": "The requested resource was not found.",
            "status_code":   404,
            "time_stamp":    datetime.now().isoformat(),
        }), 404
 
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({
            "success":       False,
            "error_message": "Method not allowed.",
            "status_code":   405,
            "time_stamp":    datetime.now().isoformat(),
        }), 405
 
    @app.errorhandler(429)
    def handle_rate_limit(e):
        return jsonify({
            "success":       False,
            "error_message": "Too many requests. Please slow down.",
            "status_code":   429,
            "time_stamp":    datetime.now().isoformat(),
        }), 429
 
    @app.errorhandler(500)
    def handle_internal_server_error(e):
        logger.error("Internal Server Error: %s", str(e))
        return jsonify({
            "success":       False,
            "error_message": "An unexpected internal server error occurred.",
            "status_code":   500,
            "time_stamp":    datetime.now().isoformat(),
        }), 500


    