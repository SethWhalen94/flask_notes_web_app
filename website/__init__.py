from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'aswefhnewufbweibf43ui4'  # Create secret key for session cookies

    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app