from api.db.mongodb import database
from api.models.user import UserIn, UserInDB
from api.core.security import get_password_hash, oauth2_scheme
from datetime import datetime
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from api.models.user import UserOut
from api.core.config import settings
from bson import ObjectId


async def get_user(email: str):
    user = await database.users.find_one({"email": email})
    if user:
        return UserInDB(**user)


async def create_user(user: UserIn):
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(
        id=str(ObjectId()),
        email=user.email,
        hashed_password=hashed_password,
        credits=10,
        last_credit_reset=datetime.now(),
        is_verified=False,
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
