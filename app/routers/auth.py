import sqlite3
from contextlib import closing

from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas import RegisterResponse, UserRegister
from app.security import hash_password

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(user: UserRegister):
    email = user.email.lower()
    try:
        with closing(get_connection()) as conn, conn:
            conn.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, hash_password(user.password)),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Користувач з таким email вже існує")
    return {"message": "Успішна реєстрація", "email": email}
