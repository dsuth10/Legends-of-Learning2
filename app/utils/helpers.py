import os
import pandas as pd
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..models.class_model import Class

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

def process_student_csv(file_path, class_id):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['username', 'password']
        
        if not all(col in df.columns for col in required_columns):
            return False, "CSV must contain columns: username and password"
        
        class_obj = Class.get(class_id)
        if not class_obj:
            return False, "Class not found"
        
        for _, row in df.iterrows():
            username = row['username']
            password = row['password']
            name = row.get('name', username)  # Use username as name if not provided
            
            # Create user if doesn't exist
            if not User.get(username):
                user = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    user_type='student',
                    name=name
                )
                user.save()
            
            # Add student to class
            class_obj.add_student(username)
        
        return True, "Students added successfully"
    except Exception as e:
        return False, f"Error processing CSV: {str(e)}"

def get_character_image_path(character_class, gender, level):
    base_path = f"static/images/characters/{character_class}/{gender}/level{level}"
    # Get the first available image for this combination
    for i in range(1, 4):
        image_path = f"{base_path}/{i}_{character_class}_{gender}_level{level}.png"
        if os.path.exists(image_path):
            return image_path
    return None 