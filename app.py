from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import pandas as pd
from datetime import datetime
from app.routes.auth import auth
from app.routes.dashboard import dashboard_bp
from app.routes.character import character
from app.routes.class_management import class_management_bp
from app.routes.codex import codex_bp
from app.routes.master_dashboard import master_dashboard_bp
from app.models.user import User

# Get the absolute path to the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            static_url_path='/static',  # Add explicit static URL path
            static_folder='static',
            template_folder='templates')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-key-please-change-in-production')  # Use environment variable with fallback

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard_bp)
app.register_blueprint(character)
app.register_blueprint(class_management_bp)
app.register_blueprint(codex_bp, url_prefix='/codex')
app.register_blueprint(master_dashboard_bp)

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Ensure static/samples directory exists
if not os.path.exists('static/samples'):
    os.makedirs('static/samples')

@login_manager.user_loader
def load_user(username):
    return User.get(username)

def save_users(users):
    with open('data/users.json', 'w') as f:
        json.dump(users, f)

def load_classes():
    try:
        with open('data/classes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_classes(classes):
    with open('data/classes.json', 'w') as f:
        json.dump(classes, f)

def load_characters():
    try:
        with open('data/characters.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error: characters.json is corrupted")
        return {}
    except IOError as e:
        print(f"Error reading characters.json: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error loading characters: {e}")
        return {}

def save_characters(characters):
    try:
        with open('data/characters.json', 'w') as f:
            json.dump(characters, f)
    except IOError as e:
        print(f"Error saving characters.json: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error saving characters: {e}")
        raise

def load_rewards():
    try:
        with open('data/rewards.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_rewards(rewards):
    with open('data/rewards.json', 'w') as f:
        json.dump(rewards, f)

def load_consequences():
    try:
        with open('data/consequences.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_consequences(consequences):
    with open('data/consequences.json', 'w') as f:
        json.dump(consequences, f)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/static/images/<path:filename>')
def serve_static(filename):
    # Split the filename into directory and file parts
    parts = filename.split('/')
    if len(parts) > 1:
        # If there are subdirectories, join all but the last part for the directory
        directory = '/'.join(parts[:-1])
        file = parts[-1]
        return send_from_directory(f'static/images/{directory}', file)
    else:
        # If no subdirectories, use the original behavior
        return send_from_directory('static/images', filename)

@app.route('/master-dashboard')
def master_dashboard():
    # Load all necessary data
    users = User.load_all()
    classes = load_classes()
    
    # Organize data for display
    teachers = [user for user in users.values() if user.get('role') == 'teacher']
    students = [user for user in users.values() if user.get('role') == 'student']
    
    # Add class information to teachers and students
    for teacher in teachers:
        teacher['classes'] = [c for c in classes.values() if c.get('teacher') == teacher['username']]
    
    for student in students:
        student_class = next((c for c in classes.values() if student['username'] in c.get('students', [])), None)
        student['class_name'] = student_class['name'] if student_class else 'No Class'
    
    return render_template('master_dashboard.html', 
                         teachers=teachers,
                         classes=list(classes.values()),
                         students=students)

if __name__ == '__main__':
    app.run(debug=True) 