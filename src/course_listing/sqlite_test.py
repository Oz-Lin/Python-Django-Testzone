import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Generate dummy admin account
admin_query = """
INSERT INTO auth_user (username, password, is_superuser, is_staff, is_active, date_joined)
VALUES (?, ?, 1, 1, 1, datetime('now'))
"""
admin_params = ('admin', 'passwordadmin')

cursor.execute(admin_query, admin_params)

# Generate dummy user accounts
user_query = """
INSERT INTO auth_user (username, password, is_superuser, is_staff, is_active, date_joined)
VALUES (?, ?, 0, 0, 1, datetime('now'))
"""
user_params = [
    ('user1', 'passworduser1'),
    ('user2', 'passworduser2'),
]

cursor.executemany(user_query, user_params)

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()