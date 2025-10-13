# Save this file as test_motor_connection.py

import asyncio
import motor.motor_asyncio
from pymongo.errors import ConnectionFailure

# --- Configuration ---
# Replace with your MongoDB connection string.
MONGO_URI = "mongodb://192.168.29.94:27017/"

async def test_mongodb_connection():
    """
    Tests the async connection to a MongoDB server using Motor.
    """
    print(f"Attempting to connect to MongoDB at {MONGO_URI}...")
    
    # Create an async client instance
    client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGO_URI, 
        serverSelectionTimeoutMS=5000
    )
    
    try:
        # The server_info() call is now an awaitable coroutine
        await client.server_info()
        print("✅ MongoDB connection successful!")
        
        # Optional: List databases asynchronously
        db_list = await client.list_database_names()
        print("Databases:", db_list)
        
    except ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the client connection
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    # Run the async function using asyncio's event loop
    asyncio.run(test_mongodb_connection())