from werkzeug.security import check_password_hash, generate_password_hash
import json

# Load the users.json file
with open('data/users.json', 'r') as f:
    users = json.load(f)

# Test student3's password
password = "password789"
student3_hash = users['student3']['password']
result = check_password_hash(student3_hash, password)
print(f"Testing password '{password}' for student3")
print(f"Current hash: {student3_hash}")
print(f"Password verification result: {result}")

# Generate a new hash for comparison
new_hash = generate_password_hash(password)
print(f"\nNew hash generated with same password: {new_hash}")
print(f"Verification of new hash: {check_password_hash(new_hash, password)}") 