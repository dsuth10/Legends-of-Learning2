import json
import os
from datetime import datetime

class Character:
    def __init__(self, username, character_class, gender, image_number=1, level=1, xp=0, health=100, power=50, gold=0):
        self.username = username
        self.character_class = character_class
        self.gender = gender
        self.image_number = image_number
        self.level = level
        self.xp = xp
        self.health = health
        self.power = power
        self.gold = gold
        self.created_at = datetime.now().isoformat()

    @staticmethod
    def load_level_progression():
        try:
            with open('data/level_progression.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "level_requirements": {"1": 0, "2": 1000},
                "level_benefits": {"2": {"health_bonus": 20, "power_bonus": 10}}
            }

    def get_next_level_xp(self):
        progression = self.load_level_progression()
        next_level = str(self.level + 1)
        return progression["level_requirements"].get(next_level, self.level * 1000)

    def check_level_up(self):
        progression = self.load_level_progression()
        next_level = str(self.level + 1)
        
        if next_level in progression["level_requirements"]:
            required_xp = progression["level_requirements"][next_level]
            if self.xp >= required_xp:
                # Apply level up benefits
                if next_level in progression["level_benefits"]:
                    benefits = progression["level_benefits"][next_level]
                    self.health = min(100, self.health + benefits.get("health_bonus", 0))
                    self.power = min(100, self.power + benefits.get("power_bonus", 0))
                
                self.level = int(next_level)
                return True
        return False

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
                xp=char_data['xp'],
                health=char_data.get('health', 100),
                power=char_data.get('power', 50),
                gold=char_data.get('gold', 0)
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
            'health': self.health,
            'power': self.power,
            'gold': self.gold,
            'created_at': self.created_at
        }
        self.save_characters(characters)

    def add_xp(self, amount):
        self.xp += amount
        if self.check_level_up():
            self.save()
        return self.level

    def add_health(self, amount):
        self.health = min(100, self.health + amount)
        self.save()

    def add_power(self, amount):
        self.power = min(100, self.power + amount)
        self.save()

    def add_gold(self, amount):
        self.gold = max(0, self.gold + amount)
        self.save() 