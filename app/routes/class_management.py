from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
import os
import pandas as pd
from ..models.class_model import Class
from ..models.user import User
from ..models.character import Character
from ..utils.helpers import process_student_csv
from werkzeug.security import generate_password_hash

class_management_bp = Blueprint('class_management', __name__, template_folder='../../templates')

@class_management_bp.route('/create_class', methods=['GET', 'POST'])
@login_required
def create_class():
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard.student_dashboard'))
    
    if request.method == 'POST':
        class_name = request.form.get('class_name')
        if not class_name:
            flash('Please enter a class name')
            return redirect(url_for('class_management.create_class'))
        
        # Create new class
        class_obj = Class(
            class_id=class_name.lower().replace(' ', '_'),
            name=class_name,
            teacher=current_user.username
        )
        class_obj.save()
        
        # Handle student CSV if provided
        if 'student_csv' in request.files:
            file = request.files['student_csv']
            if file.filename:
                if not file.filename.endswith('.csv'):
                    flash('Please upload a CSV file')
                    return redirect(url_for('class_management.create_class'))
                
                # Save file temporarily
                file_path = os.path.join('temp', file.filename)
                os.makedirs('temp', exist_ok=True)
                file.save(file_path)
                
                # Process CSV
                success, message = process_student_csv(file_path, class_obj.class_id)
                flash(message)
                
                # Clean up
                os.remove(file_path)
        
        return redirect(url_for('class_management.class_details', class_code=class_obj.class_id))
    
    return render_template('create_class.html')

@class_management_bp.route('/class/<class_code>')
@login_required
def class_details(class_code):
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard.student_dashboard'))
    
    class_obj = Class.get(class_code)
    if not class_obj or class_obj.teacher != current_user.username:
        flash('Class not found')
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    # Get student information
    students = []
    users = User.load_users()
    for username in class_obj.students:
        if username in users:
            student_info = {
                'username': username,
                'name': users[username].get('name', username),
                'character': Character.get(username)  # Load character information
            }
            students.append(student_info)
    
    return render_template('class_details.html',
                         class_name=class_obj.name,
                         class_code=class_obj.class_id,
                         students=students)

@class_management_bp.route('/class/<class_code>/delete')
@login_required
def delete_class(class_code):
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard.student_dashboard'))
    
    class_obj = Class.get(class_code)
    if not class_obj or class_obj.teacher != current_user.username:
        flash('Class not found')
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    # Delete class
    classes = Class.load_classes()
    if class_code in classes:
        del classes[class_code]
        Class.save_classes(classes)
    
    flash('Class deleted successfully')
    return redirect(url_for('dashboard.teacher_dashboard'))

@class_management_bp.route('/download_template')
@login_required
def download_template():
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard.student_dashboard'))
    
    # Create template DataFrame
    df = pd.DataFrame({
        'username': ['student1', 'student2'],
        'password': ['password1', 'password2'],
        'name': ['Student 1', 'Student 2']
    })
    
    # Save to temporary file
    os.makedirs('temp', exist_ok=True)
    template_path = os.path.join('temp', 'student_template.csv')
    df.to_csv(template_path, index=False)
    
    # Send file and clean up
    response = send_file(template_path, as_attachment=True)
    response.call_on_close(lambda: os.remove(template_path))
    return response

@class_management_bp.route('/class/<class_code>/student/<username>/edit', methods=['POST'])
@login_required
def edit_student(class_code, username):
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard.student_dashboard'))
    
    class_obj = Class.get(class_code)
    if not class_obj or class_obj.teacher != current_user.username:
        flash('Class not found')
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    if username not in class_obj.students:
        flash('Student not found')
        return redirect(url_for('class_management.class_details', class_code=class_code))
    
    # Get form data
    name = request.form.get('name')
    password = request.form.get('password')
    
    # Update user data
    users = User.load_users()
    if username in users:
        users[username]['name'] = name
        if password:  # Only update password if provided
            users[username]['password_hash'] = generate_password_hash(password)
        User.save_users(users)
        flash('Student updated successfully')
    else:
        flash('Student not found')
    
    return redirect(url_for('class_management.class_details', class_code=class_code))

@class_management_bp.route('/class/<class_code>/student/<username>/delete', methods=['POST'])
@login_required
def delete_student(class_code, username):
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard.student_dashboard'))
    
    class_obj = Class.get(class_code)
    if not class_obj or class_obj.teacher != current_user.username:
        flash('Class not found')
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    if username not in class_obj.students:
        flash('Student not found')
        return redirect(url_for('class_management.class_details', class_code=class_code))
    
    # Remove student from class
    class_obj.remove_student(username)
    
    # Delete user account
    users = User.load_users()
    if username in users:
        del users[username]
        User.save_users(users)
    
    flash('Student deleted successfully')
    return redirect(url_for('class_management.class_details', class_code=class_code)) 