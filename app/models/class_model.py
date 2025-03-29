import json
import os
from datetime import datetime

class Class:
    def __init__(self, class_id, name, teacher, students=None):
        self.class_id = class_id
        self.name = name
        self.teacher = teacher
        self.students = students or []
        self.created_at = datetime.now().isoformat()

    @staticmethod
    def get(class_id):
        classes = Class.load_classes()
        if class_id in classes:
            class_data = classes[class_id]
            return Class(
                class_id=class_id,
                name=class_data['name'],
                teacher=class_data['teacher'],
                students=class_data['students']
            )
        return None

    @staticmethod
    def load_classes():
        try:
            with open('data/classes.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_classes(classes):
        os.makedirs('data', exist_ok=True)
        with open('data/classes.json', 'w') as f:
            json.dump(classes, f, indent=4)

    def save(self):
        classes = self.load_classes()
        classes[self.class_id] = {
            'name': self.name,
            'teacher': self.teacher,
            'students': self.students,
            'created_at': self.created_at
        }
        self.save_classes(classes)

    def add_student(self, username):
        if username not in self.students:
            self.students.append(username)
            self.save()

    def remove_student(self, username):
        if username in self.students:
            self.students.remove(username)
            self.save() 