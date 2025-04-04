import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import json

# Load the CSV file
df = pd.read_csv('student_template.csv')

# Process each row
for _, row in df.iterrows():
    username = row['username']
    password = row['password']
    
    # Generate a hash for the password
    hash = generate_password_hash(password)
    
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Generated hash: {hash}")
    print()

# Load the users.json file
with open('data/users.json', 'r') as f:
    users = json.load(f)

# Check if student3 exists in the users.json file
if 'student3' in users:
    print(f"Student3 in users.json: {users['student3']}")
    print(f"Student3 password hash: {users['student3']['password']}")
    
    # Test the password
    password = "password789"
    result = check_password_hash(users['student3']['password'], password)
    print(f"Password verification result: {result}") 