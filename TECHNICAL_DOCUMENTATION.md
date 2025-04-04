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

## Important Configuration Notes

### Static Files
- Static files are served from the `static` directory
- The Flask app is configured with `static_url_path='/static'`
- Icons and images must be placed in `static/images/`
- Character images should be in `static/images/characters/`
- The Legends of Learning icon (`legends_icon.png`) must be in `static/images/`

### Blueprint Configuration
- All routes are organized into blueprints for modularity
- Blueprints must be registered with the correct `template_folder`
- When referencing routes in templates, always include the blueprint name (e.g., `auth.login`, `class_management.create_class`)

### Teacher Authentication
- Teacher registration requires a special code (default: 'TEACHER123')
- This code should be changed in production via environment variables
- Only teachers can create classes and manage students

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
│       ├── class_details.html     # Class details page
│       ├── council_chamber.html   # Council chamber interface
│       ├── create_consequence.html # Consequence creation interface
│       └── create_reward.html     # Reward creation interface
└── data/                   # Data storage directory
    ├── users.json         # User accounts and credentials
    ├── classes.json       # Class information
    ├── characters.json    # Student character data
    ├── rewards.json       # Reward system data
    └── consequences.json  # Consequence system data
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
    def __init__(self, username, character_class, gender, image_number=1, level=1, xp=0, health=100, power=50, gold=0)
    def get(username)
    def save()
    def add_xp(amount)
    def add_health(amount)
    def add_power(amount)
    def add_gold(amount)
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
- `/class/<class_code>/student/<username>/edit`: Edit student details
- `/class/<class_code>/student/<username>/delete`: Delete student from class

### Council Chamber Routes
- `/council_chamber`: Access the council chamber interface
- `/create_reward`: Create new rewards
- `/create_consequence`: Create new consequences

## Utility Functions (app/utils/helpers.py)
- `allowed_file(filename)`: Check if file extension is allowed
- `process_student_csv(file_path, class_id)`: Process student CSV file
- `get_character_image_path(character_class, gender, image_number)`: Get character image path

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
        "image_number": 1,
        "level": 1,
        "xp": 0,
        "health": 100,
        "power": 50,
        "gold": 0,
        "created_at": "ISO timestamp"
    }
}
```

### Reward Data (rewards.json)
```json
{
    "reward_id": {
        "name": "Reward Name",
        "description": "Reward Description",
        "xp": 100,
        "health": 10,
        "power": 5,
        "gold": 50,
        "class_id": "class_identifier",
        "created_at": "ISO timestamp"
    }
}
```

### Consequence Data (consequences.json)
```json
{
    "consequence_id": {
        "name": "Consequence Name",
        "description": "Consequence Description",
        "xp": -50,
        "health": -10,
        "power": -5,
        "gold": -25,
        "class_id": "class_identifier",
        "created_at": "ISO timestamp"
    }
}
```

## Field Requirements

### Rewards
- **Required Fields**:
  - `name`: Name of the reward
- **Optional Fields**:
  - `description`: Description of the reward
  - `xp`: Experience points awarded (default: 0)
  - `health`: Health points awarded (default: 0)
  - `power`: Power points awarded (default: 0)
  - `gold`: Gold coins awarded (default: 0)

### Consequences
- **Required Fields**:
  - `name`: Name of the consequence
- **Optional Fields**:
  - `description`: Description of the consequence
  - `xp`: Experience points penalty (default: 0)
  - `health`: Health points penalty (default: 0)
  - `power`: Power points penalty (default: 0)
  - `gold`: Gold coins penalty (default: 0)

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
- `image_number`: Selected character image number

### Class Details Variables
- `class_name`: Name of the class
- `class_code`: Unique identifier for the class
- `students`: List of student information dictionaries containing:
  - `username`: Student's username
  - `name`: Student's display name
  - `character`: Character information (if created)

### Council Chamber Variables
- `rewards`: List of available rewards
- `consequences`: List of available consequences
- `class_rewards`: Rewards specific to the current class
- `class_consequences`: Consequences specific to the current class
- `students`: List of students in the class with their character data

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

### Working with Templates
1. Always use `url_for()` with blueprint names for routes
2. Use the correct blueprint prefix for all routes (e.g., `auth.login`, `class_management.create_class`)
3. Include proper error handling and feedback messages
4. Ensure all forms have CSRF protection
5. Use Bootstrap classes consistently for styling

## Security Considerations
- All routes except login and create_account require authentication
- Teacher-specific routes check user_type
- Passwords are hashed before storage
- File uploads are validated for type and content
- User input is sanitized before storage
- Teacher registration code should be changed in production
- JSON data files should have proper permissions set

## Development Guidelines
1. Always use `url_for()` for generating URLs with correct blueprint names
2. Use flash messages for user feedback
3. Validate all user input
4. Handle file operations with try/except blocks
5. Use appropriate HTTP methods (GET/POST)
6. Follow Flask-Login best practices for authentication
7. Keep this technical documentation up to date
8. Test all changes with both teacher and student accounts
9. Verify static file serving configuration when making changes
10. Always clean up temporary files after processing

## Testing
- Run the application using `python run.py`
- Test all user flows (login, registration, class creation, etc.)
- Verify data persistence in JSON files
- Check error handling and user feedback
- Test with different user types (teacher/student)
- Test reward and consequence system functionality
- Verify static file serving (icons, images)
- Test student management functions (edit, delete)
- Verify class creation with and without CSV upload
- Test character creation and progression system

## Common Issues and Solutions
1. Static Files Not Loading
   - Verify static folder configuration in app.py
   - Check file paths in templates
   - Use url_for('static', filename='path') consistently
   - Clear browser cache after changes

2. Blueprint Route Errors
   - Always include blueprint name in url_for() calls
   - Check blueprint registration in app.py
   - Verify template folder paths for blueprints

3. Student Management
   - Students must be in a class before creating characters
   - Character data persists even if student is removed from class
   - Clean up character data when deleting students

4. Data Persistence
   - Always use try/except when reading/writing JSON files
   - Verify file permissions on data directory
   - Keep backup of data files during development

5. Character Display in Class Dashboard
   - Ensure the Character model is imported in class_management.py
   - Use Character.get(username) to load character information for each student
   - Verify that characters.json contains the correct data for each student

6. Password Reset
   - Use werkzeug.security.generate_password_hash() to create new password hashes
   - Update the password field in users.json with the new hash
   - Ensure the hash is generated using the same method as the application

## Deployment Considerations
1. Change default teacher registration code
2. Set proper file permissions for data files
3. Configure proper static file serving
4. Set up proper logging
5. Use environment variables for sensitive data
6. Configure proper error handling
7. Set up backup system for JSON data files

### Character Image Structure
Character images are stored in the following directory structure:
```
static/images/characters/
├── {character_class}/           # warrior, sorcerer, or druid
│   ├── {gender}/               # male or female
│   │   ├── level{level}/       # level1, level2, or level3
│   │   │   ├── {image_number}_{character_class}_{gender}_level{level}.png
```

Image naming convention:
- Format: `{image_number}_{character_class}_{gender}_level{level}.png`
- Example: `1_warrior_male_level1.png` 