from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/copy"
    mongo.init_app(app)

    from .routes import register_routes
    register_routes(app)
    
    return app
