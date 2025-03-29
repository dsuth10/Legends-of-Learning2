from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from ..models.character import Character
from ..utils.helpers import get_character_image_path

character = Blueprint('character', __name__)

@character.route('/character_creation', methods=['GET', 'POST'])
@login_required
def character_creation():
    if current_user.user_type != 'student':
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    if Character.get(current_user.username):
        return redirect(url_for('dashboard.student_dashboard'))
    
    if request.method == 'POST':
        gender = request.form.get('gender')
        
        if not gender:
            flash('Please select a gender')
            return redirect(url_for('character.character_creation'))
        
        # Store gender in session for next step
        session['character_gender'] = gender
        return redirect(url_for('character.character_class_selection'))
    
    return render_template('character_creation.html')

@character.route('/character_class_selection', methods=['GET', 'POST'])
@login_required
def character_class_selection():
    if current_user.user_type != 'student':
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    if Character.get(current_user.username):
        return redirect(url_for('dashboard.student_dashboard'))
    
    if 'character_gender' not in session:
        return redirect(url_for('character.character_creation'))
    
    if request.method == 'POST':
        character_class = request.form.get('character_class')
        
        if not character_class:
            flash('Please select a class')
            return redirect(url_for('character.character_class_selection'))
        
        # Store class in session for next step
        session['character_class'] = character_class
        return redirect(url_for('character.character_image_selection'))
    
    return render_template('character_class_selection.html', gender=session['character_gender'])

@character.route('/character_image_selection', methods=['GET', 'POST'])
@login_required
def character_image_selection():
    if current_user.user_type != 'student':
        return redirect(url_for('dashboard.teacher_dashboard'))
    
    if Character.get(current_user.username):
        return redirect(url_for('dashboard.student_dashboard'))
    
    if 'character_gender' not in session or 'character_class' not in session:
        return redirect(url_for('character.character_creation'))
    
    if request.method == 'POST':
        character_image = request.form.get('character_image')
        
        if not character_image:
            flash('Please select a character appearance')
            return redirect(url_for('character.character_image_selection'))
        
        # Create character with the selected image number
        character = Character(
            username=current_user.username,
            character_class=session['character_class'],
            gender=session['character_gender'],
            image_number=int(character_image)
        )
        character.save()
        
        # Clear session data
        session.pop('character_gender', None)
        session.pop('character_class', None)
        
        flash('Character created successfully!')
        return redirect(url_for('dashboard.student_dashboard'))
    
    return render_template('character_image_selection.html',
                         gender=session['character_gender'],
                         character_class=session['character_class']) 