# Legends of Learning

A local web application for gamifying classroom activities and tracking student progress.

## Features

- Teacher and Student user types
- Secure login system
- Class creation and management
- Student progress tracking
- Achievement system
- Activity management

## Setup

1. Install Python 3.8 or higher
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to `http://localhost:5000`

## Usage

### For Teachers

1. Create a teacher account using the "Create Account" link on the login page
   - Use the teacher code: `TEACHER123` (change this in production)
2. Log in with your credentials
3. Create a class by:
   - Clicking "Create New Class"
   - Entering a class name
   - Uploading a CSV file with student credentials
   - The CSV should have columns: `username` and `password`

### For Students

1. Log in with the credentials provided by your teacher
2. View your progress, available activities, and achievements
3. Complete activities to earn XP and unlock achievements

## Data Storage

The application uses JSON files for data storage:
- `data/users.json`: Stores user accounts and credentials
- `data/classes.json`: Stores class information and student assignments

## Security Notes

- Change the `app.secret_key` in `app.py` before deploying
- Change the teacher code in `app.py` before deploying
- The application is designed for local use only
- Passwords are hashed using Werkzeug's security functions

## Development

The application is built using:
- Flask for the backend
- Bootstrap for the frontend
- Flask-Login for user authentication
- Pandas for CSV processing 