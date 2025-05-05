from flask import Flask
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
    
    return app


