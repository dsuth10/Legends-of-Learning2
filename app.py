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

@app.route('/codex_of_conduct')
@login_required
def view_codex_of_conduct():
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard.student_dashboard'))
    
    # Get the teacher's class
    classes = load_classes()
    teacher_class = None
    teacher_class_id = None
    for class_id, class_data in classes.items():
        if class_data['teacher'] == current_user.username:
            teacher_class = class_data
            teacher_class_id = class_id
            break
    
    if not teacher_class:
        flash('Please create a class first')
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    # Load rewards and consequences for this class
    rewards = load_rewards()
    consequences = load_consequences()
    class_rewards = {k: v for k, v in rewards.items() if v.get('class_id') == teacher_class_id}
    class_consequences = {k: v for k, v in consequences.items() if v.get('class_id') == teacher_class_id}
    
    # Get list of students with their character data
    students = {}
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        with open('data/characters.json', 'r') as f:
            characters = json.load(f)
            for username in teacher_class['students']:
                if username in users:
                    students[username] = {
                        'name': users[username].get('name', username),
                        'character': characters.get(username, {})
                    }
    except FileNotFoundError:
        pass
    
    return render_template('council_chamber.html',
                         rewards=class_rewards,
                         consequences=class_consequences,
                         students=students)

@app.route('/api/rewards', methods=['POST'])
@login_required
def create_reward():
    try:
        if current_user.user_type != 'teacher':
            return jsonify({'success': False, 'message': 'Unauthorized'})
        
        # Get the teacher's class
        classes = load_classes()
        teacher_class = None
        teacher_class_id = None
        for class_id, class_data in classes.items():
            if class_data['teacher'] == current_user.username:
                teacher_class = class_data
                teacher_class_id = class_id
                break
        
        if not teacher_class:
            return jsonify({'success': False, 'message': 'No class found'})
        
        # Debug print form data
        print("Form data received:", request.form)
        
        name = request.form.get('name')
        description = request.form.get('description')
        cost = request.form.get('cost')
        
        # Debug print parsed values
        print("Parsed values:", {'name': name, 'description': description, 'cost': cost})
        
        if not name or not description or not cost:
            return jsonify({'success': False, 'message': 'Missing required fields'})
        
        try:
            cost = int(cost)
        except ValueError:
            return jsonify({'success': False, 'message': 'Cost must be a number'})
        
        if cost < 0:
            return jsonify({'success': False, 'message': 'Cost cannot be negative'})
        
        rewards = load_rewards()
        reward_id = str(len(rewards) + 1)
        
        rewards[reward_id] = {
            'name': name,
            'description': description,
            'cost': cost,
            'class_id': teacher_class_id,
            'created_at': datetime.now().isoformat()
        }
        
        save_rewards(rewards)
        return jsonify({'success': True})
        
    except Exception as e:
        print("Error in create_reward:", str(e))  # Debug print the error
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

@app.route('/api/consequences', methods=['POST'])
@login_required
def create_consequence():
    try:
        if current_user.user_type != 'teacher':
            return jsonify({'success': False, 'message': 'Unauthorized'})
        
        # Get the teacher's class
        classes = load_classes()
        teacher_class = None
        teacher_class_id = None
        for class_id, class_data in classes.items():
            if class_data['teacher'] == current_user.username:
                teacher_class = class_data
                teacher_class_id = class_id
                break
        
        if not teacher_class:
            return jsonify({'success': False, 'message': 'No class found'})
        
        # Debug print form data
        print("Form data received:", request.form)
        
        name = request.form.get('name')
        description = request.form.get('description')
        penalty = request.form.get('penalty')
        
        # Debug print parsed values
        print("Parsed values:", {'name': name, 'description': description, 'penalty': penalty})
        
        if not name or not description or not penalty:
            return jsonify({'success': False, 'message': 'Missing required fields'})
        
        try:
            penalty = int(penalty)
        except ValueError:
            return jsonify({'success': False, 'message': 'Penalty must be a number'})
        
        if penalty < 0:
            return jsonify({'success': False, 'message': 'Penalty cannot be negative'})
        
        consequences = load_consequences()
        consequence_id = str(len(consequences) + 1)
        
        consequences[consequence_id] = {
            'name': name,
            'description': description,
            'penalty': penalty,
            'class_id': teacher_class_id,
            'created_at': datetime.now().isoformat()
        }
        
        save_consequences(consequences)
        return jsonify({'success': True})
        
    except Exception as e:
        print("Error in create_consequence:", str(e))  # Debug print the error
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

@app.route('/api/rewards/<reward_id>', methods=['DELETE'])
@login_required
def delete_reward(reward_id):
    if current_user.user_type != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    rewards = load_rewards()
    if reward_id not in rewards:
        return jsonify({'success': False, 'message': 'Reward not found'})
    
    # Verify the reward belongs to the teacher's class
    classes = load_classes()
    teacher_class = None
    teacher_class_id = None
    for class_id, class_data in classes.items():
        if class_data['teacher'] == current_user.username:
            teacher_class = class_data
            teacher_class_id = class_id
            break
    
    if not teacher_class or rewards[reward_id]['class_id'] != teacher_class_id:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    del rewards[reward_id]
    save_rewards(rewards)
    return jsonify({'success': True})

@app.route('/api/consequences/<consequence_id>', methods=['DELETE'])
@login_required
def delete_consequence(consequence_id):
    if current_user.user_type != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    consequences = load_consequences()
    if consequence_id not in consequences:
        return jsonify({'success': False, 'message': 'Consequence not found'})
    
    # Verify the consequence belongs to the teacher's class
    classes = load_classes()
    teacher_class = None
    teacher_class_id = None
    for class_id, class_data in classes.items():
        if class_data['teacher'] == current_user.username:
            teacher_class = class_data
            teacher_class_id = class_id
            break
    
    if not teacher_class or consequences[consequence_id]['class_id'] != teacher_class_id:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    del consequences[consequence_id]
    save_consequences(consequences)
    return jsonify({'success': True})

@app.route('/api/rewards/assign', methods=['POST'])
@login_required
def assign_reward():
    if current_user.user_type != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    reward_id = data.get('reward_id')
    student_id = data.get('student_id')
    
    if not reward_id or not student_id:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    # Get the teacher's class
    classes = load_classes()
    teacher_class = None
    teacher_class_id = None
    for class_id, class_data in classes.items():
        if class_data['teacher'] == current_user.username:
            teacher_class = class_data
            teacher_class_id = class_id
            break
    
    if not teacher_class:
        return jsonify({'success': False, 'message': 'No class found'})
    
    # Verify the reward exists and belongs to the teacher's class
    rewards = load_rewards()
    if reward_id not in rewards or rewards[reward_id]['class_id'] != teacher_class_id:
        return jsonify({'success': False, 'message': 'Invalid reward'})
    
    # Verify the student exists in the class
    if student_id not in teacher_class.get('students', {}):
        return jsonify({'success': False, 'message': 'Student not found'})
    
    # Get the reward XP amount
    reward_xp = rewards[reward_id]['cost']
    
    # Update student's XP
    characters = load_characters()
    if student_id in characters:
        characters[student_id]['xp'] += reward_xp
        save_characters(characters)
    
    return jsonify({'success': True})

@app.route('/api/consequences/assign', methods=['POST'])
@login_required
def assign_consequence():
    if current_user.user_type != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    consequence_id = data.get('consequence_id')
    student_id = data.get('student_id')
    
    if not consequence_id or not student_id:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    # Get the teacher's class
    classes = load_classes()
    teacher_class = None
    teacher_class_id = None
    for class_id, class_data in classes.items():
        if class_data['teacher'] == current_user.username:
            teacher_class = class_data
            teacher_class_id = class_id
            break
    
    if not teacher_class:
        return jsonify({'success': False, 'message': 'No class found'})
    
    # Verify the consequence exists and belongs to the teacher's class
    consequences = load_consequences()
    if consequence_id not in consequences or consequences[consequence_id]['class_id'] != teacher_class_id:
        return jsonify({'success': False, 'message': 'Invalid consequence'})
    
    # Verify the student exists in the class
    if student_id not in teacher_class.get('students', {}):
        return jsonify({'success': False, 'message': 'Student not found'})
    
    # Get the consequence penalty
    consequence_penalty = consequences[consequence_id]['penalty']
    
    # Update student's XP
    characters = load_characters()
    if student_id in characters:
        characters[student_id]['xp'] = max(0, characters[student_id]['xp'] - consequence_penalty)
        save_characters(characters)
    
    return jsonify({'success': True})

@app.route('/create_reward')
@login_required
def view_create_reward():
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard'))
    return render_template('create_reward.html')

@app.route('/create_consequence')
@login_required
def view_create_consequence():
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard'))
    return render_template('create_consequence.html')

@app.route('/static/images/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True) 