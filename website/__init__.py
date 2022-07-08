from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app() -> Flask:
    """ This function creates the WSGI application and acts as the central
    object of the web app

    :return: the main application object
    :rtype: Flask object
    """
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'aswefhnewufbweibf43ui4'  # Create secret key for session cookies
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(DB_NAME)  # Register URI for database in app config
    db.init_app(app) # Initialize database to be used with our app


    from .views import views
    from .auth import auth

    # Register blueprints for endpoints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(id: int):
        """ load user when logging in to app

        :param id: user id
        :type id: int
        :return: user object
        :rtype: User
        """
        return User.query.get(int(id))

    return app

def create_database(app: Flask):
    """ This method checks if the database exists, and if not, it creates it

    :param app: The main flask application
    :type app: Flask
    """

    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")