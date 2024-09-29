from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated
from datetime import datetime
from bson import ObjectId


class UserBase(BaseModel):
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: Annotated[str, Field(default_factory=lambda: str(ObjectId()), alias="_id")]
    credits: int
    last_credit_reset: datetime
    is_active: bool

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class UserInDB(UserOut):
    hashed_password: str
    verification_token: str


class Token(BaseModel):
    access_token: str
    token_type: str

class VerificationRequest(BaseModel):
    token: str