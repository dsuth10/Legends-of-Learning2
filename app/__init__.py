from flask import Flask, send_from_directory
from flask_login import LoginManager
from .models.user import User
from .routes.auth import auth
from .routes.dashboard import dashboard_bp
from .routes.character import character
from .routes.class_management import class_management_bp
from .routes.codex import codex_bp
from .routes.master_dashboard import master_dashboard_bp
import os

def create_app():
    app = Flask(__name__, 
                static_url_path='/static',
                static_folder='static',
                template_folder='templates')
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
    app.register_blueprint(codex_bp, url_prefix='/codex')
    app.register_blueprint(master_dashboard_bp)
    
    # Add route for serving static files from subdirectories
    @app.route('/static/images/<path:filename>')
    def serve_static(filename):
        # Get the absolute path to the static directory
        static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
        
        # Split the filename into directory and file parts
        parts = filename.split('/')
        if len(parts) > 1:
            # If there are subdirectories, join all but the last part for the directory
            directory = '/'.join(parts[:-1])
            file = parts[-1]
            return send_from_directory(os.path.join(static_dir, 'images', directory), file)
        else:
            # If no subdirectories, use the original behavior
            return send_from_directory(os.path.join(static_dir, 'images'), filename)
    
    return app 