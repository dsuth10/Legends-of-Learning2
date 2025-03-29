# Legends of Learning - Technical Documentation

## Tech Stack

### Backend
- **Framework**: Flask (Python 3.x)
- **Authentication**: Flask-Login
- **Data Storage**: JSON files
- **Data Processing**: pandas (for CSV handling)
- **Security**: Werkzeug (password hashing)

### Frontend
- **Template Engine**: Jinja2
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JS

## Project Structure

```
Legends of Learning/
├── run.py                    # Application entry point
├── app/                      # Main application package
│   ├── __init__.py          # Application factory
│   ├── models/              # Data models
│   │   ├── user.py          # User model
│   │   ├── character.py     # Character model
│   │   └── class_model.py   # Class model
│   ├── routes/              # Route handlers
│   │   ├── auth.py          # Authentication routes
│   │   ├── dashboard.py     # Dashboard routes
│   │   ├── character.py     # Character management routes
│   │   └── class_management.py  # Class management routes
│   ├── utils/               # Utility functions
│   │   └── helpers.py       # Helper functions
│   ├── static/              # Static files
│   │   ├── images/         # Image assets
│   │   └── samples/        # Sample files (e.g., CSV templates)
│   └── templates/          # HTML templates
│       ├── base.html       # Base template with common elements
│       ├── login.html      # Login page
│       ├── create_account.html  # Account creation page
│       ├── teacher_dashboard.html  # Teacher dashboard
│       ├── student_dashboard.html  # Student dashboard
│       ├── character_creation.html # Character creation page
│       ├── character_class_selection.html  # Character class selection
│       ├── character_image_selection.html  # Character image selection
│       └── class_details.html     # Class details page
└── data/                   # Data storage directory
    ├── users.json         # User accounts and credentials
    ├── classes.json       # Class information
    └── characters.json    # Student character data
```

## Data Models

### User Model (app/models/user.py)
```python
class User(UserMixin):
    def __init__(self, username, password_hash, user_type, name=None)
    def get(username)
    def check_password(password)
    def save()
```

### Character Model (app/models/character.py)
```python
class Character:
    def __init__(self, username, character_class, gender, level=1, xp=0)
    def get(username)
    def save()
    def add_xp(amount)
```

### Class Model (app/models/class_model.py)
```python
class Class:
    def __init__(self, class_id, name, teacher, students=None)
    def get(class_id)
    def save()
    def add_student(username)
    def remove_student(username)
```

## Routes

### Authentication Routes (app/routes/auth.py)
- `/login`: Handle user login
- `/logout`: Handle user logout
- `/create_account`: Create new teacher account

### Dashboard Routes (app/routes/dashboard.py)
- `/dashboard`: Main dashboard (redirects based on user type)
- `/teacher_dashboard`: Teacher-specific dashboard
- `/student_dashboard`: Student-specific dashboard

### Character Routes (app/routes/character.py)
- `/character_creation`: Start character creation process
- `/character_class_selection`: Select character class and gender
- `/character_image_selection`: Select character appearance

### Class Management Routes (app/routes/class_management.py)
- `/create_class`: Create new class with student CSV
- `/class/<class_code>`: View class details
- `/class/<class_code>/delete`: Delete a class
- `/download_template`: Download student CSV template

## Utility Functions (app/utils/helpers.py)
- `allowed_file(filename)`: Check if file extension is allowed
- `process_student_csv(file_path, class_id)`: Process student CSV file
- `get_character_image_path(character_class, gender, level)`: Get character image path

## Data Structures

### User Data (users.json)
```json
{
    "username": {
        "password": "hashed_password",
        "user_type": "teacher|student",
        "name": "Display Name"
    }
}
```

### Class Data (classes.json)
```json
{
    "class_id": {
        "name": "Class Name",
        "teacher": "teacher_username",
        "students": ["student1", "student2", ...],
        "created_at": "ISO timestamp"
    }
}
```

### Character Data (characters.json)
```json
{
    "username": {
        "class": "warrior|sorcerer|druid",
        "gender": "male|female",
        "level": 1,
        "xp": 0,
        "created_at": "ISO timestamp"
    }
}
```

## Template Variables

### Common Variables (base.html)
- `current_user`: Current logged-in user object
- `user_type`: Type of user ("teacher" or "student")

### Teacher Dashboard Variables
- `classes`: Dictionary of classes taught by the teacher

### Student Dashboard Variables
- `progress`: Progress to next level (0-100)
- `level`: Current character level
- `xp`: Current experience points
- `next_level_xp`: XP needed for next level
- `character_class`: Character class (warrior/sorcerer/druid)
- `gender`: Character gender

### Class Details Variables
- `class_name`: Name of the class
- `class_code`: Unique identifier for the class
- `students`: List of student information dictionaries

## Making Changes

### Adding New Features
1. Add new model in `app/models/` if needed
2. Add new routes in `app/routes/`
3. Create necessary templates in `app/templates/`
4. Add any required static files
5. Update this technical documentation

### Modifying Existing Features
1. Update relevant model in `app/models/`
2. Modify corresponding routes in `app/routes/`
3. Update templates in `app/templates/`
4. Update this technical documentation

### Adding New Data Fields
1. Update relevant model in `app/models/`
2. Update data structures in JSON files
3. Update templates to display new data
4. Add data migration logic if needed
5. Update this technical documentation

## Security Considerations
- All routes except login and create_account require authentication
- Teacher-specific routes check user_type
- Passwords are hashed before storage
- File uploads are validated for type and content
- User input is sanitized before storage

## Development Guidelines
1. Always use `url_for()` for generating URLs
2. Use flash messages for user feedback
3. Validate all user input
4. Handle file operations with try/except blocks
5. Use appropriate HTTP methods (GET/POST)
6. Follow Flask-Login best practices for authentication
7. Keep this technical documentation up to date

## Testing
- Run the application using `python run.py`
- Test all user flows (login, registration, class creation, etc.)
- Verify data persistence in JSON files
- Check error handling and user feedback
- Test with different user types (teacher/student) 