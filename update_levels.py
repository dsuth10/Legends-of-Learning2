import json
import os
from app.models.character import Character

def update_character_levels():
    """
    Update all existing characters to properly level up based on their XP
    using the new level progression system.
    """
    print("Starting character level update...")
    
    # Load all characters
    characters = Character.load_characters()
    updated_count = 0
    
    for username, char_data in characters.items():
        # Create a Character object
        character = Character(
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
        
        # Get the current level
        old_level = character.level
        
        # Check if character should level up
        if character.check_level_up():
            updated_count += 1
            print(f"Updated {username} from level {old_level} to level {character.level}")
            print(f"  XP: {character.xp}, Health: {character.health}, Power: {character.power}")
        
        # Save the character
        character.save()
    
    print(f"Level update complete. Updated {updated_count} characters.")

if __name__ == "__main__":
    update_character_levels() 