from datetime import datetime, timedelta

from bcrypt import checkpw, gensalt, hashpw
from fastapi import Depends
from jose import jwt

import app.api.auth.crud_auth as crud_auth
from app.config.config import get_settings
from app.database.get_db import SessionLocal, get_db


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(
        plain_password.encode('utf-8'), hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


def authenticate(
    email: str, password: str, db: SessionLocal = Depends(get_db)
):
    user = crud_auth.get_user_by_email(db=db, email_user=email)
    if not user:
        return False
    if not verify_password(password, user.senha):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().SECRET_KEY,
        algorithm=get_settings().ALGORITHM,
    )
    return encoded_jwt
