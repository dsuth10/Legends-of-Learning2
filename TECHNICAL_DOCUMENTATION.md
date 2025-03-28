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
├── app.py                 # Main application file
├── data/                  # Data storage directory
│   ├── users.json        # User accounts and credentials
│   ├── classes.json      # Class information
│   └── characters.json   # Student character data
├── static/               # Static files
│   ├── images/          # Image assets
│   └── samples/         # Sample files (e.g., CSV templates)
└── templates/           # HTML templates
    ├── base.html        # Base template with common elements
    ├── login.html       # Login page
    ├── create_account.html  # Account creation page
    ├── teacher_dashboard.html  # Teacher dashboard
    ├── student_dashboard.html  # Student dashboard
    ├── character_creation.html # Character creation page
    └── class_details.html     # Class details page
```

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

## Key Components

### User Management
- **User Class**: `User(UserMixin)`
  - Attributes:
    - `username`: Unique identifier
    - `password_hash`: Hashed password
    - `user_type`: "teacher" or "student"
    - `name`: Display name (defaults to username)

### Authentication
- **Login Manager**: Flask-Login
- **Session Management**: Flask session
- **Password Hashing**: Werkzeug's `generate_password_hash` and `check_password_hash`

### Data Loading/Saving Functions
- `load_users()`: Load user data from users.json
- `save_users(users)`: Save user data to users.json
- `load_classes()`: Load class data from classes.json
- `save_classes(classes)`: Save class data to classes.json
- `load_characters()`: Load character data from characters.json
- `save_characters(characters)`: Save character data to characters.json

## Routes

### Authentication Routes
- `/login`: Handle user login
- `/logout`: Handle user logout
- `/create_account`: Create new teacher account

### Dashboard Routes
- `/dashboard`: Main dashboard (redirects based on user type)
- `/teacher_dashboard`: Teacher-specific dashboard
- `/student_dashboard`: Student-specific dashboard

### Class Management Routes
- `/create_class`: Create new class with student CSV
- `/class/<class_code>`: View class details
- `/class/<class_code>/delete`: Delete a class
- `/class/<class_code>/student/<username>/edit`: Edit student information
- `/class/<class_code>/student/<username>/delete`: Remove student from class

### Character Management Routes
- `/character_creation`: Create student character

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
- `activities`: List of available activities
- `achievements`: List of earned achievements

### Class Details Variables
- `class_name`: Name of the class
- `class_code`: Unique identifier for the class
- `students`: List of student information dictionaries

## Making Changes

### Adding New Features
1. Add new route in `app.py`
2. Create necessary template if required
3. Update data structures in JSON files if needed
4. Add any required static files (CSS, JS, images)
5. Update this technical documentation

### Modifying Existing Features
1. Update route logic in `app.py`
2. Modify corresponding template
3. Update data structures if necessary
4. Update this technical documentation

### Adding New Data Fields
1. Update relevant JSON data structure
2. Modify User class if adding user-related fields
3. Update templates to display new data
4. Add data migration logic if needed
5. Update this technical documentation

## Documentation Maintenance

### When to Update
This technical documentation should be updated whenever you:
1. Add new features or routes
2. Modify existing functionality
3. Change data structures
4. Add new dependencies
5. Update the project structure
6. Modify security measures
7. Change development guidelines

### What to Update
1. **Project Structure**: Add/remove files and directories
2. **Data Structures**: Update JSON schemas
3. **Routes**: Add/modify route descriptions
4. **Template Variables**: Update available variables
5. **Key Components**: Add/modify component descriptions
6. **Tech Stack**: Update dependencies and versions
7. **Development Guidelines**: Add/modify best practices
8. **Security Considerations**: Update security measures

### How to Update
1. Keep the documentation in sync with code changes
2. Use clear, concise language
3. Include code examples where relevant
4. Maintain consistent formatting
5. Update all affected sections
6. Review changes for accuracy
7. Test documentation against actual code

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
- Run the application in debug mode for development
- Test all user flows (login, registration, class creation, etc.)
- Verify data persistence in JSON files
- Check error handling and user feedback
- Test with different user types (teacher/student) 