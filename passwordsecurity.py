import re
import hashlib
from collections import Counter
import sqlite3
import os
import secrets

# Initialize SQLite database
def initialize_db():
    conn = sqlite3.connect("password_security.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    ''')
    conn.commit()
    update_db_schema(conn)  # Update schema if necessary
    return conn

# Update database schema if needed
def update_db_schema(conn):
    cursor = conn.cursor()
    try:
        # Add the 'salt' column if it does not exist
        cursor.execute("ALTER TABLE users ADD COLUMN salt TEXT NOT NULL DEFAULT ''")
        conn.commit()
        print("Database schema updated successfully.")
    except sqlite3.OperationalError:
        print("Column 'salt' already exists or cannot be added.")

# Password strength evaluation
strength_criteria = {
    "length": lambda pwd: len(pwd) >= 8,
    "uppercase": lambda pwd: bool(re.search(r"[A-Z]", pwd)),
    "lowercase": lambda pwd: bool(re.search(r"[a-z]", pwd)),
    "digits": lambda pwd: bool(re.search(r"\d", pwd)),
    "special": lambda pwd: bool(re.search(r"[@$!%*?&#]", pwd)),
}

def evaluate_password_strength(password):
    score = sum(criteria(password) for criteria in strength_criteria.values())
    violations = []
    if len(password) < 8:
        violations.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        violations.append("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        violations.append("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        violations.append("Password must contain at least one digit.")
    if not re.search(r"[@$!%*?&#]", password):
        violations.append("Password must contain at least one special character.")

    if score < 3:
        return "Weak", violations
    elif score == 3:
        return "Moderate", violations
    else:
        return "Strong", violations

# Generate salted hash for password storage
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Main execution
def main():
    conn = initialize_db()

    print("Create a new user and test the password:")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Evaluate password strength
    strength, violations = evaluate_password_strength(password)
    print(f"Password Strength: {strength}")
    if violations:
        print("Policy Violations:")
        for violation in violations:
            print(f"- {violation}")

    # Check for password reuse in the database
    cursor = conn.cursor()
    cursor.execute("SELECT password, salt FROM users")
    existing_passwords = cursor.fetchall()
    salt = secrets.token_hex(16)
    hashed_password = hash_password(password, salt)

    if any(hashed_password == hash_password(row[0], row[1]) for row in existing_passwords):
        print("Password is reused! Consider choosing a different one.")
    else:
        print("Password is unique.")
        # Insert the new user into the database
        cursor.execute('''
            INSERT INTO users (username, password, salt)
            VALUES (?, ?, ?)
        ''', (username, hashed_password, salt))
        conn.commit()
        print("User added successfully.")

    # Display all users
    print("\nExisting Users:")
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"- {user[0]}")

    conn.close()


if __name__ == "__main__":
    main()
