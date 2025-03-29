from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
import os
import pandas as pd
from ..models.class_model import Class
from ..models.user import User
from ..utils.helpers import process_student_csv

class_management_bp = Blueprint('class_management', __name__)

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
    for username in class_obj.students:
        student_info = {
            'username': username,
            'character': None  # We'll add character info later if needed
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