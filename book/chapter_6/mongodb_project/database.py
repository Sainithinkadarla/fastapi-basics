from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

motor_client = AsyncIOMotorClient("mongodb://172.17.0.3:27017")

database = motor_client['sample']

def get_db() -> AsyncIOMotorDatabase:
    return database