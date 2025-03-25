import re
import hashlib
import sqlite3
import secrets
import matplotlib.pyplot as plt
import datetime

# --- Database Initialization ---
def initialize_db():
    """
    Initialize the SQLite database and create necessary tables if they don't exist.
    """
    conn = sqlite3.connect("password_security.db")
    cursor = conn.cursor()

    # Drop users table (TEMPORARY FIX) to ensure the schema is correct
    cursor.execute("DROP TABLE IF EXISTS users")  

    # Create users table with password strength and violation count columns
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            password_strength TEXT NOT NULL,
            violation_count INTEGER NOT NULL DEFAULT 0,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_reports (
            id INTEGER PRIMARY KEY,
            report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            weak_passwords INTEGER NOT NULL,
            moderate_passwords INTEGER NOT NULL,
            strong_passwords INTEGER NOT NULL,
            violations INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    return conn

# --- Password Strength Evaluation ---
strength_criteria = {
    "length": lambda pwd: len(pwd) >= 8,
    "uppercase": lambda pwd: bool(re.search(r"[A-Z]", pwd)),
    "lowercase": lambda pwd: bool(re.search(r"[a-z]", pwd)),
    "digits": lambda pwd: bool(re.search(r"\d", pwd)),
    "special": lambda pwd: bool(re.search(r"[@$!%*?&#]", pwd)),
}

def evaluate_password_strength(password):
    """
    Evaluate password strength and return strength level and list of violations.
    """
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

# --- Password Hashing ---
def hash_password(password, salt):
    """
    Hash the password with a salt and return the hashed password.
    """
    return hashlib.sha256((password + salt).encode()).hexdigest()

# --- Data Logging Functions ---
def log_password_data(conn, username, password, salt, password_strength, violations_count):
    """
    Log password strength and violations data into the database.
    """
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, salt, password_strength, violation_count)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, salt, password_strength, violations_count))
    conn.commit()

def generate_password_report(conn):
    """
    Generate and log a report on password strength and violations in the database.
    """
    cursor = conn.cursor()

    cursor.execute("SELECT password_strength, COUNT(*) FROM users GROUP BY password_strength")
    result = cursor.fetchall()
    
    cursor.execute("SELECT SUM(violation_count) FROM users")
    violations = cursor.fetchone()[0]

    weak_passwords = sum(1 for r in result if r[0] == 'Weak')
    moderate_passwords = sum(1 for r in result if r[0] == 'Moderate')
    strong_passwords = sum(1 for r in result if r[0] == 'Strong')

    cursor.execute('''
        INSERT INTO password_reports (weak_passwords, moderate_passwords, strong_passwords, violations)
        VALUES (?, ?, ?, ?)
    ''', (weak_passwords, moderate_passwords, strong_passwords, violations))
    conn.commit()

def fetch_password_report_data(conn):
    """
    Fetch all the password reports data from the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT report_date, weak_passwords, moderate_passwords, strong_passwords, violations FROM password_reports")
    return cursor.fetchall()

# --- Matplotlib Visualization Functions ---
def plot_password_trends(report_data):
    """
    Plot password strength and violations trends using matplotlib.
    """
    dates = [entry[0] for entry in report_data]
    weak = [entry[1] for entry in report_data]
    moderate = [entry[2] for entry in report_data]
    strong = [entry[3] for entry in report_data]
    violations = [entry[4] for entry in report_data]

    dates = [datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]

    # Use plt.figure instead of matplotlib.figure.Figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.bar(dates, weak, width=0.2, label='Weak', align='center', color='red')
    ax1.bar(dates, moderate, width=0.2, label='Moderate', align='edge', color='yellow')
    ax1.bar(dates, strong, width=0.2, label='Strong', align='edge', color='green')
    ax1.set_title('Password Strength Trends Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Password Count')
    ax1.legend()

    ax2.plot(dates, violations, label='Violations', color='blue', marker='o')
    ax2.set_title('Password Violations Over Time')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Violations Count')
    ax2.legend()

    fig.tight_layout()
    
    # Show the plot
    plt.show()
    
# --- Main Program Execution ---
def main():
    """
    Main function to execute the password security analysis.
    """
    # Initialize the database
    conn = initialize_db()

    # Get user input for username and password
    print("Create a new user and test the password:")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Evaluate password strength and check for violations
    strength, violations = evaluate_password_strength(password)
    print(f"Password Strength: {strength}")
    print(f"Policy Violations: {len(violations)} violations")

    # Generate a salt and hash the password
    salt = secrets.token_hex(16)
    hashed_password = hash_password(password, salt)

    # Check for password reuse
    cursor = conn.cursor()
    cursor.execute("SELECT password, salt FROM users")
    existing_passwords = cursor.fetchall()

    if any(hashed_password == hash_password(row[0], row[1]) for row in existing_passwords):
        print("Password is reused! Consider choosing a different one.")
    else:
        print("Password is unique.")

        # Insert new user into the database
        cursor.execute('''
            INSERT INTO users (username, password, salt, password_strength, violation_count)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, hashed_password, salt, strength, len(violations)))
        conn.commit()
        print("User added successfully.")

    # Generate a password report
    generate_password_report(conn)

    # Fetch the report data for plotting
    report_data = fetch_password_report_data(conn)

    # Plot the password trends
    plot_password_trends(report_data)

    # Display all users (optional)
    print("\nExisting Users:")
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    for user in users:
        print(f"- {user[0]}")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()


    #testing