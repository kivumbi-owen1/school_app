from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import timedelta

db = SQLAlchemy()

bcrypt=Bcrypt()

login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY']='2ebf88db72ed6c6a4d7a1a2ac7a3affc'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///school.db'
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = True  # If using HTTPS
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
