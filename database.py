import sqlite3


# ==========================================
# CREATE DATABASE & TABLES
# ==========================================
def create_database():
    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    # ---------- USERS TABLE ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    # ---------- TRANSACTIONS TABLE ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    connection.commit()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("\nTables in database:")
    for table in tables:
        print(table[0])

    connection.close()


# ==========================================
# USER FUNCTIONS
# ==========================================
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
        SELECT *
        FROM users
        WHERE email = ? AND password = ?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# ==========================================
# TRANSACTION FUNCTIONS
# ==========================================
def add_transaction(
        user_id,
        transaction_type,
        amount,
        category,
        description,
        date):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO transactions
        (user_id, type, amount, category, description, date)

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            transaction_type,
            amount,
            category,
            description,
            date
        )
    )

    connection.commit()
    connection.close()

    print("Transaction added successfully!")


# ==========================================
# DASHBOARD FUNCTIONS
# ==========================================
def get_total_income(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id = ?
        AND type = 'income'
    """, (user_id,))

    total = cursor.fetchone()[0]

    connection.close()

    return total if total else 0


def get_total_expense(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
    """, (user_id,))

    total = cursor.fetchone()[0]

    connection.close()

    return total if total else 0


def get_current_balance(user_id):

    income = get_total_income(user_id)
    expense = get_total_expense(user_id)

    return income - expense


def get_recent_transaction(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT type, category, amount
        FROM transactions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    transaction = cursor.fetchone()

    connection.close()

    if transaction:

        transaction_type, category, amount = transaction

        sign = "+" if transaction_type == "income" else "-"

        return f"{category}   {sign}₹{amount}"

    return "No transactions yet."


# ==========================================
# HISTORY FUNCTIONS
# ==========================================
def get_all_transactions(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            type,
            category,
            amount,
            description,
            date
        FROM transactions
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    transactions = cursor.fetchall()

    connection.close()

    return transactions


# ==========================================
# DELETE TRANSACTION
# ==========================================
def delete_transaction(transaction_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM transactions
        WHERE id = ?
    """, (transaction_id,))

    connection.commit()
    connection.close()

    print("Transaction deleted successfully!")


# ==========================================
# UPDATE TRANSACTION
# ==========================================
def update_transaction(
        transaction_id,
        transaction_type,
        amount,
        category,
        description,
        date):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions
        SET
            type = ?,
            amount = ?,
            category = ?,
            description = ?,
            date = ?
        WHERE id = ?
    """,
    (
        transaction_type,
        amount,
        category,
        description,
        date,
        transaction_id
    ))

    connection.commit()
    connection.close()

    print("Transaction updated successfully!")


# ==========================================
# TEST DATABASE
# ==========================================
if __name__ == "__main__":
    create_database()