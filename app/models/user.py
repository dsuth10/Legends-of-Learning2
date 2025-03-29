from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

class User(UserMixin):
    def __init__(self, username, password_hash, user_type, name=None):
        self.username = username
        self.password_hash = password_hash
        self.user_type = user_type
        self.name = name or username

    def get_id(self):
        return self.username

    @classmethod
    def get(cls, username):
        users = cls.load_users()
        if username in users:
            user_data = users[username]
            return cls(
                username=username,
                password_hash=user_data['password'],
                user_type=user_data['user_type'],
                name=user_data.get('name')
            )
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def load_users():
        try:
            with open('data/users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_users(users):
        os.makedirs('data', exist_ok=True)
        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=4)

    def save(self):
        users = self.load_users()
        users[self.username] = {
            'password': self.password_hash,
            'user_type': self.user_type,
            'name': self.name
        }
        self.save_users(users) 