from databases import Database
from fastapi import FastAPI
from contextlib import asynccontextmanager

#pip install databases aiosqlite

database = Database('sqlite:///test.db')

async def create_table():
    await database.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT);
    """)

    count = await database.fetch_val("SELECT COUNT(*) FROM users")

    if count == 0:
        await database.execute("INSERT INTO users (username) VALUES ('John')")
        await database.execute("INSERT INTO users (username) VALUES ('mon')")


@asynccontextmanager
async def lifespan(app):
    print("Startup actions executing....")
    # on startup actions
    await database.connect()
    await create_table()
    print("startup actions executed")
    yield
    #on shutdown actions
    print("Bye!!!")
    await database.disconnect()

testdb = FastAPI(lifespan=lifespan)
    
@testdb.get("/db")
async def get_users():
    rows = await database.fetch_all("SELECT * FROM users;")
    return {"data": rows}