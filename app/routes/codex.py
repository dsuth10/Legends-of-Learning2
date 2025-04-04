from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..models.character import Character
import json
from datetime import datetime

codex_bp = Blueprint('codex', __name__, template_folder='../../templates')

def load_classes():
    try:
        with open('data/classes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_rewards():
    try:
        with open('data/rewards.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_consequences():
    try:
        with open('data/consequences.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_rewards(rewards):
    with open('data/rewards.json', 'w') as f:
        json.dump(rewards, f)

def save_consequences(consequences):
    with open('data/consequences.json', 'w') as f:
        json.dump(consequences, f)

def save_characters(characters):
    with open('data/characters.json', 'w') as f:
        json.dump(characters, f)

def load_characters():
    try:
        with open('data/characters.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@codex_bp.route('/')
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

@codex_bp.route('/create_reward')
@login_required
def view_create_reward():
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard'))
    return render_template('create_reward.html')

@codex_bp.route('/create_consequence')
@login_required
def view_create_consequence():
    if current_user.user_type != 'teacher':
        return redirect(url_for('dashboard'))
    return render_template('create_consequence.html')

@codex_bp.route('/api/rewards/create', methods=['POST'])
@login_required
def create_reward():
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
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    xp = data.get('xp', 0)
    health = data.get('health', 0)
    power = data.get('power', 0)
    gold = data.get('gold', 0)
    
    if not name or not description:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    rewards = load_rewards()
    reward_id = str(len(rewards) + 1)
    
    rewards[reward_id] = {
        'name': name,
        'description': description,
        'xp': xp,
        'health': health,
        'power': power,
        'gold': gold,
        'class_id': teacher_class_id,
        'created_at': datetime.now().isoformat()
    }
    
    save_rewards(rewards)
    return jsonify({'success': True})

@codex_bp.route('/api/consequences/create', methods=['POST'])
@login_required
def create_consequence():
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
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    xp = data.get('xp', 0)
    health = data.get('health', 0)
    power = data.get('power', 0)
    gold = data.get('gold', 0)
    
    if not name or not description:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    consequences = load_consequences()
    consequence_id = str(len(consequences) + 1)
    
    consequences[consequence_id] = {
        'name': name,
        'description': description,
        'xp': xp,
        'health': health,
        'power': power,
        'gold': gold,
        'class_id': teacher_class_id,
        'created_at': datetime.now().isoformat()
    }
    
    save_consequences(consequences)
    return jsonify({'success': True})

@codex_bp.route('/api/rewards/<reward_id>', methods=['DELETE'])
@login_required
def delete_reward(reward_id):
    if current_user.user_type != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    rewards = load_rewards()
    if reward_id in rewards:
        del rewards[reward_id]
        save_rewards(rewards)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Reward not found'})

@codex_bp.route('/api/consequences/<consequence_id>', methods=['DELETE'])
@login_required
def delete_consequence(consequence_id):
    if current_user.user_type != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    consequences = load_consequences()
    if consequence_id in consequences:
        del consequences[consequence_id]
        save_consequences(consequences)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Consequence not found'})

@codex_bp.route('/api/rewards/assign', methods=['POST'])
@login_required
def assign_reward():
    if current_user.user_type != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    reward_id = data.get('reward_id')
    student_id = data.get('student_id')
    
    if not reward_id or not student_id:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    rewards = load_rewards()
    if reward_id not in rewards:
        return jsonify({'success': False, 'message': 'Reward not found'})
    
    reward = rewards[reward_id]
    characters = load_characters()
    
    if student_id not in characters:
        return jsonify({'success': False, 'message': 'Student not found'})
    
    character = characters[student_id]
    
    # Update character stats
    character['xp'] = character.get('xp', 0) + reward.get('xp', 0)
    character['health'] = min(100, character.get('health', 100) + reward.get('health', 0))
    character['power'] = min(100, character.get('power', 50) + reward.get('power', 0))
    character['gold'] = character.get('gold', 0) + reward.get('gold', 0)
    
    save_characters(characters)
    
    return jsonify({
        'success': True,
        'effects': {
            'xp': reward.get('xp', 0),
            'health': reward.get('health', 0),
            'power': reward.get('power', 0),
            'gold': reward.get('gold', 0)
        }
    })

@codex_bp.route('/api/consequences/assign', methods=['POST'])
@login_required
def assign_consequence():
    if current_user.user_type != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.get_json()
    consequence_id = data.get('consequence_id')
    student_id = data.get('student_id')
    
    if not consequence_id or not student_id:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    consequences = load_consequences()
    if consequence_id not in consequences:
        return jsonify({'success': False, 'message': 'Consequence not found'})
    
    consequence = consequences[consequence_id]
    characters = load_characters()
    
    if student_id not in characters:
        return jsonify({'success': False, 'message': 'Student not found'})
    
    character = characters[student_id]
    
    # Update character stats
    character['xp'] = max(0, character.get('xp', 0) + consequence.get('xp', 0))
    character['health'] = max(0, character.get('health', 100) + consequence.get('health', 0))
    character['power'] = max(0, character.get('power', 50) + consequence.get('power', 0))
    character['gold'] = max(0, character.get('gold', 0) + consequence.get('gold', 0))
    
    save_characters(characters)
    
    return jsonify({
        'success': True,
        'effects': {
            'xp': consequence.get('xp', 0),
            'health': consequence.get('health', 0),
            'power': consequence.get('power', 0),
            'gold': consequence.get('gold', 0)
        }
    }) 