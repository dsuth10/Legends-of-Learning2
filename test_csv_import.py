from app.utils.helpers import process_student_csv
from app.models.user import User
from app.models.class_model import Class
import pandas as pd
import os
from werkzeug.security import check_password_hash
import json

def setup_test():
    # Create test class
    test_class = Class('test_class', 'Test Class', 'test_teacher')
    test_class.save()
    
    return 'student_template.csv', 'test_class'

def cleanup_test():
    # Remove test users
    users = User.load_users()
    test_usernames = ['student1', 'student2', 'student3']
    for username in test_usernames:
        if username in users:
            del users[username]
    User.save_users(users)
    
    # Remove test class
    classes = Class.load_classes()
    if 'test_class' in classes:
        del classes['test_class']
    Class.save_classes(classes)

def verify_student_creation(username, password):
    users = User.load_users()
    if username not in users:
        print(f"❌ User {username} not found in users.json")
        return False
    
    user_data = users[username]
    if not check_password_hash(user_data['password'], password):
        print(f"❌ Password verification failed for {username}")
        return False
    
    print(f"✓ User {username} created successfully with correct password")
    return True

def verify_class_assignment(class_id, username):
    class_obj = Class.get(class_id)
    if not class_obj:
        print(f"❌ Class {class_id} not found")
        return False
    
    if username not in class_obj.students:
        print(f"❌ Student {username} not found in class {class_id}")
        return False
    
    print(f"✓ Student {username} correctly assigned to class {class_id}")
    return True

def run_tests():
    print("Starting CSV import tests with student_template.csv...")
    
    # Setup
    csv_path, class_id = setup_test()
    print("\n1. Test setup complete")
    
    # Test CSV processing
    success, message = process_student_csv(csv_path, class_id)
    print(f"\n2. CSV Processing Result: {message}")
    if not success:
        print("❌ CSV processing failed")
        cleanup_test()
        return
    
    # Verify student accounts
    print("\n3. Verifying student accounts:")
    test_data = [
        ('student1', 'password123'),
        ('student2', 'password456'),
        ('student3', 'password789')
    ]
    
    all_users_valid = True
    for username, password in test_data:
        if not verify_student_creation(username, password):
            all_users_valid = False
    
    # Verify class assignments
    print("\n4. Verifying class assignments:")
    all_assignments_valid = True
    for username, _ in test_data:
        if not verify_class_assignment(class_id, username):
            all_assignments_valid = False
    
    # Final results
    print("\nTest Results:")
    print("✓ CSV Processing:", "Passed" if success else "Failed")
    print("✓ User Creation:", "Passed" if all_users_valid else "Failed")
    print("✓ Class Assignment:", "Passed" if all_assignments_valid else "Failed")
    
    # Cleanup
    cleanup_test()
    print("\nTest cleanup complete")

if __name__ == '__main__':
    run_tests() 