"""User authentication module for handling login and registration."""

users = {}
current_user = None

def register(username: str, password: str, email: str) -> bool:
    """Register a new user with a username, password, and email."""
    global users
    if username in users:
        return False
    if not validate_email(email):
        return False
    if not is_strong_password(password):
        return False
    users[username] = {'password': password, 'email': email}
    return True

def login(username: str, password: str) -> bool:
    """Authenticate a user with their username and password."""
    global current_user
    if username in users and users[username]['password'] == password:
        current_user = username
        return True
    return False

def logout() -> bool:
    """Log out the currently authenticated user."""
    global current_user
    if current_user is None:
        return False
    current_user = None
    return True

def validate_email(email: str) -> bool:
    """Check if the email format is valid."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password: str) -> bool:
    """Check if the password is strong enough."""
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)