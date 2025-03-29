from flask import Flask
from flask_login import LoginManager
from .models.user import User
from .routes.auth import auth
from .routes.dashboard import dashboard_bp
from .routes.character import character
from .routes.class_management import class_management_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(username):
        return User.get(username)
    
    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(character)
    app.register_blueprint(class_management_bp)
    
    return app 