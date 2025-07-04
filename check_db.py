# This script checks if the SQLite database 'clerq.db' exists and lists its tables.
import sqlite3

conn = sqlite3.connect('db/clerq.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:", tables)

conn.close()
