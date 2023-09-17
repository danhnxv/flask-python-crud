# Import necessary modules and packages
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_restful import Api
from dotenv import load_dotenv
import os
from config import TestingConfig, DevelopmentConfig

# Load environment variables from a .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get the value of FLASK_ENV environment variable
flask_env = os.getenv("FLASK_ENV", default="development")

# Configure the app based on the environment
if flask_env == "development":
    app.config.from_object(DevelopmentConfig)
elif flask_env == "testing":
    app.config.from_object(TestingConfig)

# Create a blueprint for the API routes
api_bp = Blueprint("main", __name__)
api = Api(api_bp)

# Register the blueprint with the app and set the URL prefix
app.register_blueprint(api_bp, url_prefix="/api")

# Initialize the SQLAlchemy instance with the app
db = SQLAlchemy(app)

# Initialize database migration with the app and db instance
migrate = Migrate(app, db)

# Import models and RESTful resources
from app import models
from app.restapi import TaskResource, TaskUpdateResource

# Add API resources
api.add_resource(TaskResource, "/tasks")
api.add_resource(TaskUpdateResource, "/tasks/<string:task_id>")
