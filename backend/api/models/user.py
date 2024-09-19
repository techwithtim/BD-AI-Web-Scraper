from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: EmailStr
    credits: int


class UserInDB(UserOut):
    hashed_password: str
    last_credit_reset: datetime
    is_verified: bool = False

    def verify_password(self, password: str):
        from app.core.security import verify_password

        return verify_password(password, self.hashed_password)


class Token(BaseModel):
    access_token: str
    token_type: str
