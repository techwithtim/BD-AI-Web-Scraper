from motor.motor_asyncio import AsyncIOMotorClient
from api.core.config import settings


client = AsyncIOMotorClient(settings.MONGODB_URL)
database = client[settings.DB_NAME]


async def connect_to_mongo():
    try:
        await client.admin.command("ping")
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


async def close_mongo_connection():
    client.close()
    print("Closed MongoDB connection")
