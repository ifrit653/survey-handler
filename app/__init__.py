from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    from app import models
    from app.routes import bp as api_bp
    app.register_blueprint(api_bp)

    return app

