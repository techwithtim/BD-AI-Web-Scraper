from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.core.security import create_access_token, get_current_user
from api.models.user import UserIn, UserOut, Token
from api.db.mongodb import get_user, create_user, update_user_credits
from datetime import timedelta
from api.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: UserIn):
    db_user = await get_user(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(user)
    return UserOut(email=new_user.email, credits=new_user.credits)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.post("/reset_credits", response_model=UserOut)
async def reset_credits(current_user: UserOut = Depends(get_current_user)):
    updated_user = await update_user_credits(current_user.email)
    if updated_user:
        return updated_user
    raise HTTPException(status_code=400, detail="Failed to reset credits")
