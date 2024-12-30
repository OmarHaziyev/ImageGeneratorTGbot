import sqlite3
import logging

# Configure logging for SQLite errors
logging.basicConfig(filename="sqlite_errors.log", level=logging.ERROR, format="%(asctime)s - %(message)s")

# Initialize SQLite database
try:
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        telegram_id INTEGER UNIQUE
    )
    ''')
    conn.commit()
except sqlite3.Error as e:
    logging.error(f"Database connection error: {e}")


# Function to add user to the database
def add_user(username, telegram_id):
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, telegram_id) VALUES (?, ?)",
            (username, telegram_id),
        )
        conn.commit()
    except sqlite3.OperationalError as e:
        logging.error(f"Operational Error: {e}")
    except sqlite3.Error as e:
        logging.error(f"Database Error: {e}")


# Function to close the database connection
def close_connection():
    try:
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Error closing the database: {e}")
