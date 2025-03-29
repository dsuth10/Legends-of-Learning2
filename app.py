from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Ensure static/samples directory exists
if not os.path.exists('static/samples'):
    os.makedirs('static/samples')

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username, password_hash, user_type, name=None):
        self.username = username
        self.password_hash = password_hash
        self.user_type = user_type
        self.name = name or username  # Use username as name if not provided

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
            if username in users:
                user_data = users[username]
                return User(username, user_data['password'], user_data['user_type'], user_data.get('name', username))
    except FileNotFoundError:
        pass
    return None

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

def save_characters(characters):
    with open('data/characters.json', 'w') as f:
        json.dump(characters, f)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
                if username in users and check_password_hash(users[username]['password'], password):
                    user = User(username, users[username]['password'], users[username]['user_type'], users[username].get('name', username))
                    login_user(user)
                    
                    # Check if student needs to create a character
                    if user.user_type == 'student':
                        characters = load_characters()
                        if username not in characters:
                            return redirect(url_for('character_creation'))
                    
                    return redirect(url_for('dashboard'))
        except FileNotFoundError:
            pass
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/character_creation', methods=['GET', 'POST'])
@login_required
def character_creation():
    if current_user.user_type != 'student':
        return redirect(url_for('dashboard'))
    
    characters = load_characters()
    if current_user.username in characters:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        gender = request.form.get('gender')
        
        if not gender:
            flash('Please select a gender')
            return redirect(url_for('character_creation'))
        
        # Store gender in session for next step
        session['character_gender'] = gender
        return redirect(url_for('character_class_selection'))
    
    return render_template('character_creation.html')

@app.route('/character_class_selection', methods=['GET', 'POST'])
@login_required
def character_class_selection():
    if current_user.user_type != 'student':
        return redirect(url_for('dashboard'))
    
    characters = load_characters()
    if current_user.username in characters:
        return redirect(url_for('dashboard'))
    
    if 'character_gender' not in session:
        return redirect(url_for('character_creation'))
    
    if request.method == 'POST':
        character_class = request.form.get('character_class')
        gender = request.form.get('gender')
        
        # Debug logging
        print(f"Form data received in class selection:")
        print(f"character_class: {character_class}")
        print(f"gender: {gender}")
        print(f"All form data: {request.form}")
        
        if not character_class or not gender:
            flash('Please select a class')
            return redirect(url_for('character_class_selection'))
        
        # Store class in session for next step
        session['character_class'] = character_class
        return redirect(url_for('character_image_selection'))
    
    return render_template('character_class_selection.html', gender=session['character_gender'])

@app.route('/character_image_selection', methods=['GET', 'POST'])
@login_required
def character_image_selection():
    if current_user.user_type != 'student':
        return redirect(url_for('dashboard'))
    
    characters = load_characters()
    if current_user.username in characters:
        return redirect(url_for('dashboard'))
    
    if 'character_gender' not in session or 'character_class' not in session:
        return redirect(url_for('character_creation'))
    
    if request.method == 'POST':
        character_class = request.form.get('character_class')
        gender = request.form.get('gender')
        character_image = request.form.get('character_image')
        
        # Debug logging
        print(f"Form data received:")
        print(f"character_class: {character_class}")
        print(f"gender: {gender}")
        print(f"character_image: {character_image}")
        
        if not character_class or not gender or not character_image:
            flash('Please select a character appearance')
            return redirect(url_for('character_image_selection'))
        
        # Create character data
        characters[current_user.username] = {
            'class': character_class,
            'gender': gender,
            'level': 1,
            'xp': 0,
            'image': f"{character_image}_{character_class}_{gender}_level1.png",
            'created_at': datetime.now().isoformat()
        }
        save_characters(characters)
        
        # Debug logging
        print(f"Saved character data: {characters[current_user.username]}")
        
        # Clear session data
        session.pop('character_gender', None)
        session.pop('character_class', None)
        
        flash('Character created successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('character_image_selection.html', 
                         gender=session['character_gender'],
                         character_class=session['character_class'])

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        teacher_code = request.form.get('teacher_code')
        name = request.form.get('name', username)  # Get name from form, default to username
        
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        
        if username in users:
            flash('Username already exists')
            return redirect(url_for('create_account'))
        
        if teacher_code != 'TEACHER123':  # This should be a secure teacher code in production
            flash('Invalid teacher code')
            return redirect(url_for('create_account'))
        
        users[username] = {
            'password': generate_password_hash(password),
            'user_type': 'teacher',
            'name': name
        }
        save_users(users)
        flash('Account created successfully')
        return redirect(url_for('login'))
    
    return render_template('create_account.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'teacher':
        classes = load_classes()
        teacher_classes = {class_id: class_data for class_id, class_data in classes.items() 
                         if class_data['teacher'] == current_user.username}
        return render_template('teacher_dashboard.html', classes=teacher_classes)
    else:
        # Load student's character data
        characters = load_characters()
        character = characters.get(current_user.username, {})
        
        # For students, we'll need to load their progress data
        return render_template('student_dashboard.html',
                             progress=character.get('xp', 0) % 100,  # Progress to next level
                             level=character.get('level', 1),
                             xp=character.get('xp', 0),
                             next_level_xp=100,
                             character_class=character.get('class', ''),
                             gender=character.get('gender', ''),
                             image=character.get('image', ''),
                             activities=[],
                             achievements=[])

@app.route('/class/<class_code>')
@login_required
def class_details(class_code):
    if current_user.user_type != 'teacher':
        flash('Access denied. Teachers only.', 'danger')
        return redirect(url_for('student_dashboard'))
    
    classes = load_classes()
    if class_code not in classes:
        flash('Class not found.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    class_data = classes[class_code]
    
    # Load character information for each student
    students = []
    characters = load_characters()
    
    # Load all users data
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    
    for username in class_data['students']:
        if username in users:
            student_info = {
                'name': users[username].get('name', username),
                'username': username,
                'character': characters.get(username)
            }
            students.append(student_info)
    
    return render_template('class_details.html', 
                         class_name=class_data['name'],
                         class_code=class_code,
                         students=students)

@app.route('/class/<class_id>/delete', methods=['POST'])
@login_required
def delete_class(class_id):
    if current_user.user_type != 'teacher':
        flash('Only teachers can delete classes')
        return redirect(url_for('dashboard'))
    
    classes = load_classes()
    if class_id not in classes:
        flash('Class not found')
        return redirect(url_for('dashboard'))
    
    class_data = classes[class_id]
    if class_data['teacher'] != current_user.username:
        flash('You do not have permission to delete this class')
        return redirect(url_for('dashboard'))
    
    # Get list of students in this class
    students_in_class = class_data['students']
    
    # Remove class
    del classes[class_id]
    save_classes(classes)
    
    # Check if students are in any other class
    all_students = set()
    for c in classes.values():
        all_students.update(c['students'])
    
    # Delete student accounts that are not in any other class
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    
    for username in students_in_class:
        if username not in all_students and username in users:
            del users[username]
    
    # Save updated users data
    save_users(users)
    
    # Also delete character data for students not in any other class
    try:
        with open('data/characters.json', 'r') as f:
            characters = json.load(f)
    except FileNotFoundError:
        characters = {}
    
    for username in students_in_class:
        if username not in all_students and username in characters:
            del characters[username]
    
    # Save updated characters data
    save_characters(characters)
    
    flash('Class deleted successfully')
    return redirect(url_for('dashboard'))

@app.route('/create_class', methods=['POST'])
@login_required
def create_class():
    if current_user.user_type != 'teacher':
        flash('Only teachers can create classes')
        return redirect(url_for('dashboard'))
    
    class_name = request.form.get('class_name')
    if not class_name:
        flash('Class name is required')
        return redirect(url_for('dashboard'))
    
    if 'student_csv' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('dashboard'))
    
    file = request.files['student_csv']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('dashboard'))
    
    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file')
        return redirect(url_for('dashboard'))
    
    try:
        df = pd.read_csv(file)
        if 'username' not in df.columns or 'password' not in df.columns:
            flash('CSV must contain username and password columns')
            return redirect(url_for('dashboard'))
        
        # Create student accounts
        users = {}
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            pass
        
        for _, row in df.iterrows():
            username = row['username']
            if username not in users:
                users[username] = {
                    'password': generate_password_hash(row['password']),
                    'user_type': 'student',
                    'name': row.get('name', username)  # Use name from CSV if available, otherwise use username
                }
        
        save_users(users)
        
        # Create class
        classes = load_classes()
        class_id = f"{current_user.username}_{class_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        classes[class_id] = {
            'name': class_name,
            'teacher': current_user.username,
            'students': df['username'].tolist(),
            'created_at': datetime.now().isoformat()
        }
        save_classes(classes)
        
        flash('Class created successfully')
    except Exception as e:
        flash(f'Error creating class: {str(e)}')
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/class/<class_code>/student/<username>/edit', methods=['POST'])
@login_required
def edit_student(class_code, username):
    if current_user.user_type != 'teacher':
        flash('Access denied. Teachers only.', 'danger')
        return redirect(url_for('student_dashboard'))
    
    classes = load_classes()
    if class_code not in classes:
        flash('Class not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    class_data = classes[class_code]
    if username not in class_data['students']:
        flash('Student not found in this class.', 'danger')
        return redirect(url_for('class_details', class_code=class_code))
    
    # Load users data
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    
    if username not in users:
        flash('Student account not found.', 'danger')
        return redirect(url_for('class_details', class_code=class_code))
    
    # Update student information
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    
    if new_name:
        users[username]['name'] = new_name
    
    if new_password:
        users[username]['password'] = generate_password_hash(new_password)
    
    # Save updated user data
    with open('data/users.json', 'w') as f:
        json.dump(users, f)
    
    flash('Student information updated successfully.', 'success')
    return redirect(url_for('class_details', class_code=class_code))

@app.route('/class/<class_code>/student/<username>/delete', methods=['POST'])
@login_required
def delete_student(class_code, username):
    if current_user.user_type != 'teacher':
        flash('Access denied. Teachers only.', 'danger')
        return redirect(url_for('student_dashboard'))
    
    classes = load_classes()
    if class_code not in classes:
        flash('Class not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    class_data = classes[class_code]
    if username not in class_data['students']:
        flash('Student not found in this class.', 'danger')
        return redirect(url_for('class_details', class_code=class_code))
    
    # Remove student from class
    class_data['students'].remove(username)
    classes[class_code] = class_data
    save_classes(classes)
    
    # Check if student is in any other class
    all_students = set()
    for c in classes.values():
        all_students.update(c['students'])
    
    # If student is not in any other class, delete their account
    if username not in all_students:
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        
        if username in users:
            del users[username]
            with open('data/users.json', 'w') as f:
                json.dump(users, f)
    
    flash('Student removed from class successfully.', 'success')
    return redirect(url_for('class_details', class_code=class_code))

if __name__ == '__main__':
    app.run(debug=True) 