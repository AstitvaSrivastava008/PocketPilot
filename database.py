import sqlite3


def create_database():
    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    connection.commit()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in database:")
    print(tables)

    connection.close()


def add_user(name, email, password):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """,
        (name, email, password)
    )

    connection.commit()
    connection.close()

    print("User added successfully!")
def login_user(email, password):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email = ? AND password = ?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user

if __name__ == "__main__":
    create_database()