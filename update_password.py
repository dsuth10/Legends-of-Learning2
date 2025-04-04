from werkzeug.security import generate_password_hash
import json

# Generate a new hash for the password "password789"
password = "password789"
new_hash = generate_password_hash(password)

# Load the users.json file
with open('data/users.json', 'r') as f:
    users = json.load(f)

# Update student3's password
if 'student3' in users:
    users['student3']['password'] = new_hash
    
    # Save the updated users.json file
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)
    
    print(f"Updated student3's password hash to: {new_hash}")
else:
    print("Student3 not found in users.json") 