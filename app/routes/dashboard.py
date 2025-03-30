from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.class_model import Class
from ..models.character import Character
from ..models.user import User
import json

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../../templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'teacher':
        return redirect(url_for('dashboard.teacher_dashboard'))
    return redirect(url_for('dashboard.student_dashboard'))

@dashboard_bp.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard.student_dashboard'))
    
    classes = Class.load_classes()
    teacher_classes = {
        class_id: class_data 
        for class_id, class_data in classes.items() 
        if class_data['teacher'] == current_user.username
    }
    return render_template('teacher_dashboard.html', classes=teacher_classes)

@dashboard_bp.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.user_type != 'student':
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    character = Character.get(current_user.username)
    if not character:
        return redirect(url_for('character.character_creation'))
    
    # Calculate progress to next level
    next_level_xp = character.level * 1000  # Simple XP calculation
    progress = (character.xp / next_level_xp) * 100 if next_level_xp > 0 else 0
    
    return render_template('student_dashboard.html',
                         character_class=character.character_class,
                         gender=character.gender,
                         level=character.level,
                         xp=character.xp,
                         next_level_xp=next_level_xp,
                         progress=progress,
                         image=f"{character.image_number}_{character.character_class}_{character.gender}_level1.png") 