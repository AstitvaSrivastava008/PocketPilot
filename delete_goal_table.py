import sqlite3

connection = sqlite3.connect("data/pocketpilot.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS savings_goal")

connection.commit()
connection.close()

print("✅ savings_goal table deleted successfully!")