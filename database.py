import sqlite3


# ==========================================
# CREATE DATABASE & TABLES
# ==========================================
def create_database():

    import os

    print("Database:", os.path.abspath("data/pocketpilot.db"))

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    # ---------- USERS TABLE ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        theme TEXT DEFAULT 'Light',
        currency TEXT DEFAULT '₹'
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

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    # ---------- SAVINGS GOAL TABLE ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS savings_goal (

        user_id INTEGER PRIMARY KEY,

        goal_name TEXT NOT NULL,

        goal_amount REAL NOT NULL,

        saved_amount REAL DEFAULT 0,

        saving_percentage REAL NOT NULL,

        target_date TEXT,

        goal_completed INTEGER DEFAULT 0,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    connection.commit()

    # ==========================================
    # DATABASE MIGRATION
    # ==========================================
    try:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN theme TEXT DEFAULT 'Light'
        """)
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN currency TEXT DEFAULT '₹'
        """)
    except sqlite3.OperationalError:
        pass

    connection.commit()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

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
# GET USER DETAILS
# ==========================================
def get_user(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return user


# ==========================================
# UPDATE USER NAME
# ==========================================
def update_user_name(user_id, new_name):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET name = ?
        WHERE id = ?
    """, (
        new_name,
        user_id
    ))

    connection.commit()
    connection.close()
# ==========================================
# VERIFY PASSWORD
# ==========================================
def verify_password(user_id, password):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE id = ?
        AND password = ?
    """, (
        user_id,
        password
    ))

    result = cursor.fetchone()

    connection.close()

    return result is not None


# ==========================================
# UPDATE PASSWORD
# ==========================================
def update_password(user_id, new_password):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE id = ?
    """, (
        new_password,
        user_id
    ))

    connection.commit()
    connection.close()
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
# ANALYTICS FUNCTIONS
# ==========================================
def get_transaction_count(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id = ?
    """, (user_id,))

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_total_savings(user_id):

    return get_total_income(user_id) - get_total_expense(user_id)


def get_expense_by_category(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM transactions
        WHERE
            user_id = ?
            AND type = 'expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (user_id,))

    data = cursor.fetchall()

    connection.close()

    return data


# ==========================================
# HIGHEST EXPENSE CATEGORY
# ==========================================
def get_highest_expense_category(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM transactions
        WHERE
            user_id = ?
            AND type = 'expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    return result


# ==========================================
# TOTAL EXPENSE CATEGORIES
# ==========================================
def get_expense_category_count(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT category)
        FROM transactions
        WHERE
            user_id = ?
            AND type = 'expense'
    """, (user_id,))

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ==========================================
# CURRENT BALANCE
# ==========================================
def get_balance(user_id):

    return get_total_income(user_id) - get_total_expense(user_id)


# ==========================================
# INCOME VS EXPENSE
# ==========================================
def get_income_vs_expense(user_id):

    return (
        get_total_income(user_id),
        get_total_expense(user_id)
    )


# ==========================================
# SAVINGS GOAL
# ==========================================
def save_goal(
        user_id,
        goal_name,
        goal_amount,
        saving_percentage,
        target_date):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO savings_goal (
            user_id,
            goal_name,
            goal_amount,
            saved_amount,
            saving_percentage,
            target_date,
            goal_completed
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET

            goal_name = excluded.goal_name,
            goal_amount = excluded.goal_amount,
            saving_percentage = excluded.saving_percentage,
            target_date = excluded.target_date,
            goal_completed = 0
    """, (
        user_id,
        goal_name,
        goal_amount,
        0,
        saving_percentage,
        target_date,
        0
    ))

    connection.commit()
    connection.close()

# ==========================================
# UPDATE SAVED AMOUNT
# ==========================================
def update_saved_amount(user_id, income_amount):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            saved_amount,
            goal_amount,
            saving_percentage
        FROM savings_goal
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if result:

        saved_amount, goal_amount, saving_percentage = result

        # Calculate how much of the income should be saved
        amount_to_save = (
            income_amount * saving_percentage
        ) / 100

        # Do not allow savings to exceed the goal amount
        new_saved = min(
            saved_amount + amount_to_save,
            goal_amount
        )

        cursor.execute("""
            UPDATE savings_goal
            SET saved_amount = ?
            WHERE user_id = ?
        """, (
            new_saved,
            user_id
        ))

    connection.commit()
    connection.close()
# ==========================================
# GET SAVINGS GOAL
# ==========================================
def get_goal(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            goal_name,
            goal_amount,
            saved_amount,
            saving_percentage,
            target_date,
            goal_completed
        FROM savings_goal
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    return result
# ==========================================
# MARK GOAL COMPLETED
# ==========================================
def mark_goal_completed(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE savings_goal
        SET goal_completed = 1
        WHERE user_id = ?
    """, (user_id,))

    connection.commit()
    connection.close()


# ==========================================
# CHECK GOAL COMPLETED
# ==========================================
def is_goal_completed(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT goal_completed
        FROM savings_goal
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return bool(result[0])

    return False
# ==========================================
# DELETE SAVINGS GOAL
# ==========================================
def delete_goal(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM savings_goal
        WHERE user_id = ?
    """, (user_id,))

    connection.commit()
    connection.close()
# ==========================================
# UPDATE THEME
# ==========================================
def update_theme(user_id, theme):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET theme = ?
        WHERE id = ?
    """, (
        theme,
        user_id
    ))

    connection.commit()
    connection.close()


# ==========================================
# GET THEME
# ==========================================
def get_theme(user_id):

    connection = sqlite3.connect("data/pocketpilot.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT theme
        FROM users
        WHERE id = ?
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return "Light"
# ==========================================
# TEST DATABASE
# ==========================================
if __name__ == "__main__":
    create_database()