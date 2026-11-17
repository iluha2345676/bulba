import re

from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not (8 <= len(v) <= 24):
            raise ValueError("Довжина від 8 до 24 символів")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Потрібна хоча б одна велика літера")
        if not re.search(r"[a-z]", v):
            raise ValueError("Потрібна хоча б одна мала літера")
        if not re.search(r"\d", v):
            raise ValueError("Потрібна хоча б одна цифра")
        if re.search(r"[@\"'<>]", v):
            raise ValueError("Містить заборонені символи (@, \", ', <, >)")
        return v


class RegisterResponse(BaseModel):
    message: str
    email: EmailStr
