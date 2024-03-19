import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the auth_user table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS auth_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    is_superuser INTEGER NOT NULL,
    is_staff INTEGER NOT NULL,
    is_active INTEGER NOT NULL,
    date_joined DATETIME NOT NULL,
    first_name TEXT,
    last_name TEXT,
    email TEXT
)
"""
cursor.execute(create_table_query)

# Generate dummy admin account
admin_query = """
INSERT INTO auth_user (username, password, is_superuser, is_staff, is_active, date_joined, first_name, last_name, email)
VALUES (?, ?, 1, 1, 1, datetime('now'), ?, ?, ?)
"""
admin_params = ('admin_test', 'passwordadmin', 'admun_first_name', 'admun_last_name', 'admuntest@gmail.com')

cursor.execute(admin_query, admin_params)

# Generate dummy user accounts
user_query = """
INSERT INTO auth_user (username, password, is_superuser, is_staff, is_active, date_joined, first_name, last_name, email)
VALUES (?, ?, 0, 0, 1, datetime('now'), ?, ?, ?)
"""
user_params = [
    ('user1_test', 'passworduser1', 'user1_first_name', 'user1_last_name', 'user1test@gmail.com'),
    ('user2_test', 'passworduser2', 'user2_first_name', 'user2_last_name', 'user2test@gmail.com'),
]

cursor.executemany(user_query, user_params)

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()