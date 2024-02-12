from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import sys

sys.path.append(str(BASE_DIR))

from datetime import date

from pydantic import BaseModel, Field, EmailStr

from src.database.models import Role



class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_data: str = None


class ContactUpdatedModel(BaseModel):
    update: bool = False


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_data: str = None

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=12)
    email: EmailStr
    password: str = Field(min_length=3, max_length=10)


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: str
    avatar: str
    roles: Role

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr