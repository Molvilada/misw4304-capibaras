import os
from flask import Flask
from db import db

def get_rds_url():
    if not all(
        key in os.environ
        for key in [
            "RDS_USERNAME",
            "RDS_PASSWORD",
            "RDS_HOST",
            "RDS_PORT",
            "RDS_DB_NAME",
        ]
    ):
        return None

    return f"postgresql+pg8000://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOST']}:{os.environ['RDS_PORT']}/{os.environ['RDS_DB_NAME']}"

# Create the Flask application
def create_app(database=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = database or get_rds_url()

    if app.config["SQLALCHEMY_DATABASE_URI"] is None:
        print("Please set the RDS environment variables")
        exit(1)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register the blueprints

    return app
