from api.db.mongodb import database
from api.models.user import UserIn, UserInDB
from api.core.security import get_password_hash, oauth2_scheme
from datetime import datetime
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from api.models.user import UserOut
from api.core.config import settings
from bson import ObjectId


STARTING_CREDITS = 10

async def get_user(email: str):
    user = await database.users.find_one({"email": email})
    if user:
        return UserInDB(**user)


async def create_user(user: UserIn, verification_token):
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(
        id=str(ObjectId()),
        email=user.email,
        hashed_password=hashed_password,
        credits=STARTING_CREDITS,
        last_credit_reset=datetime.now(),
        is_active=False,
        verification_token=verification_token,
    )
    
    await database.users.insert_one(db_user.dict(by_alias=True))
    return db_user


async def update_user_credits(email: str, credit_change: int):
    user = await get_user(email)
    if user:
        new_credits = max(
            user.credits + credit_change, 0
        )  # Ensure credits don't go below 0
        result = await database.users.update_one(
            {"email": email}, {"$set": {"credits": new_credits}}
        )
        if result.modified_count == 1:
            updated_user = await database.users.find_one({"email": email})
            return UserOut(**updated_user)
    return None

async def verify_user(email: str, is_active=True):
    user = await get_user(email)
    if user:
        result = await database.users.update_one(
            {"email": email}, {"$set": {"is_active": is_active}}
        )
        if result.modified_count == 1:
            updated_user = await database.users.find_one({"email": email})
            return UserOut(**updated_user)
    return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(email)
    if user is None:
        raise credentials_exception
    return user

async def get_user_by_verification_token(token: str):
    user = await database.users.find_one({
        "verification_token": token,
    })
    if user:
        return UserInDB(**user)
    return None