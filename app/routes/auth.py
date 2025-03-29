from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from ..models.user import User
import json
import os

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get(username)
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        teacher_code = request.form.get('teacher_code')
        name = request.form.get('name', username)
        
        if User.get(username):
            flash('Username already exists')
            return redirect(url_for('auth.create_account'))
        
        if teacher_code != 'TEACHER123':  # This should be a secure teacher code in production
            flash('Invalid teacher code')
            return redirect(url_for('auth.create_account'))
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            user_type='teacher',
            name=name
        )
        user.save()
        flash('Account created successfully')
        return redirect(url_for('auth.login'))
    return render_template('create_account.html') 