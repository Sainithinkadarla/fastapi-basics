from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

motor_client = AsyncIOMotorClient("mongodb://192.168.29.94:27017")

database = motor_client['sample']

def get_db() -> AsyncIOMotorDatabase:
    return database