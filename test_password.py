from werkzeug.security import check_password_hash
import json

# Load the users.json file
with open('data/users.json', 'r') as f:
    users = json.load(f)

# Get student3's password hash
student3_hash = users['student3']['password']

# Test the password
password = "password789"
result = check_password_hash(student3_hash, password)

print(f"Password verification result: {result}")
print(f"Student3 hash: {student3_hash}") 