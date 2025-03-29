import json
import os
from datetime import datetime

class Character:
    def __init__(self, username, character_class, gender, image_number=1, level=1, xp=0):
        self.username = username
        self.character_class = character_class
        self.gender = gender
        self.image_number = image_number
        self.level = level
        self.xp = xp
        self.created_at = datetime.now().isoformat()

    @staticmethod
    def get(username):
        characters = Character.load_characters()
        if username in characters:
            char_data = characters[username]
            return Character(
                username=username,
                character_class=char_data['class'],
                gender=char_data['gender'],
                image_number=char_data.get('image_number', 1),
                level=char_data['level'],
                xp=char_data['xp']
            )
        return None

    @staticmethod
    def load_characters():
        try:
            with open('data/characters.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_characters(characters):
        os.makedirs('data', exist_ok=True)
        with open('data/characters.json', 'w') as f:
            json.dump(characters, f, indent=4)

    def save(self):
        characters = self.load_characters()
        characters[self.username] = {
            'class': self.character_class,
            'gender': self.gender,
            'image_number': self.image_number,
            'level': self.level,
            'xp': self.xp,
            'created_at': self.created_at
        }
        self.save_characters(characters)

    def add_xp(self, amount):
        self.xp += amount
        # Level up logic can be added here
        self.save() 