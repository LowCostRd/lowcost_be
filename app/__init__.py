from flask import Flask, jsonify

from app.exception.copy_exception import CopyException
from .extensions import mongo
from dotenv import load_dotenv
import os



def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["MONGO_POOL_SIZE"] = os.getenv("MONGO_POOL_SIZE")
    app.config["MONGO_MAX_POOL_SIZE"] = os.getenv("MONGO_MAX_POOL_SIZE")
    mongo.init_app(app)

    from .routes import register_routes
    register_routes(app)

    @app.errorhandler(CopyException)
    def handle_copy_exception(error):
        return jsonify(error.to_dict()),error.code
    
    
    
    return app


