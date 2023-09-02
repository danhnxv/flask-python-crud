from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_restful import Api


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object("app.config.DevelopmentConfig")

api_bp = Blueprint("main", __name__)
api = Api(api_bp)
app.register_blueprint(api_bp, url_prefix="/api")

db = SQLAlchemy(app)  # flask-sqlalchemy
migrate = Migrate(app, db)  # this

from app import models
from app.restapi import *


api.add_resource(TaskResource, "/tasks")
api.add_resource(TaskUpdateResource, "/tasks/<string:task_id>")

if __name__ == "__main__":
    app.debug = True
    app.run()
