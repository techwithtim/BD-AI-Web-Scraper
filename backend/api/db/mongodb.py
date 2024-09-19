from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.models.user import UserIn, UserInDB
from app.core.security import get_password_hash
from datetime import datetime, timedelta

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


async def get_user(email: str):
    user = await database.users.find_one({"email": email})
    if user:
        return UserInDB(**user)


async def create_user(user: UserIn):
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(
        email=user.email,
        hashed_password=hashed_password,
        credits=10,
        last_credit_reset=datetime.utcnow(),
        is_verified=False,
    )
    await database.users.insert_one(db_user.dict())
    return db_user


async def update_user_credits(email: str):
    now = datetime.now()
    user = await get_user(email)
    if user and (now - user.last_credit_reset) >= timedelta(days=1):
        result = await database.users.update_one(
            {"email": email}, {"$set": {"credits": 10, "last_credit_reset": now}}
        )
        if result.modified_count == 1:
            return UserInDB(**await database.users.find_one({"email": email}))
    return None
