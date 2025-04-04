from werkzeug.security import generate_password_hash

# Generate a hash for the password "password789"
password = "password789"
hash = generate_password_hash(password)

print(f"Generated hash for 'password789': {hash}") 