from app.database import Base, engine
import app.models
import sqlite3

print("Creating database.......")
Base.metadata.create_all(bind = engine)
print("Database created sucessfully!")

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
tables = cursor.fetchall()
conn.close()
print("Tables in the databases: ", tables )
