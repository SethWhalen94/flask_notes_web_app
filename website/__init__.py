from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'aswefhnewufbweibf43ui4'  # Create secret key for session cookies
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(DB_NAME)  # Register URI for database in app config
    db.init_app(app) # Initialize database to be used with our app

    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app