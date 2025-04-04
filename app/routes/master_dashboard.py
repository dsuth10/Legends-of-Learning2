from flask import Blueprint, render_template, redirect, url_for, flash
from ..models.user import User
import json
import os

master_dashboard_bp = Blueprint('master_dashboard', __name__)

def load_classes():
    try:
        with open('data/classes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def reset_data():
    # Reset users
    User.save_users({})
    
    # Reset classes
    with open('data/classes.json', 'w') as f:
        json.dump({}, f)
        
    # Reset characters if exists
    if os.path.exists('data/characters.json'):
        with open('data/characters.json', 'w') as f:
            json.dump({}, f)
            
    # Reset rewards if exists
    if os.path.exists('data/rewards.json'):
        with open('data/rewards.json', 'w') as f:
            json.dump({}, f)
            
    # Reset consequences if exists
    if os.path.exists('data/consequences.json'):
        with open('data/consequences.json', 'w') as f:
            json.dump({}, f)

@master_dashboard_bp.route('/reset-all-data')
def reset_all_data():
    reset_data()
    flash('All data has been reset successfully!', 'success')
    return redirect(url_for('master_dashboard.master_dashboard'))

@master_dashboard_bp.route('/master-dashboard')
def master_dashboard():
    # Load all necessary data
    users = User.load_users()
    classes = load_classes()
    
    # Organize data for display
    teachers = [{'username': username, **user_data} 
               for username, user_data in users.items() 
               if user_data.get('user_type') == 'teacher']
    students = [{'username': username, **user_data} 
               for username, user_data in users.items() 
               if user_data.get('user_type') == 'student']
    
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