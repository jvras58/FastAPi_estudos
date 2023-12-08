from datetime import datetime, timedelta

from bcrypt import checkpw, gensalt, hashpw
from fastapi import Depends
from jose import jwt

import app.api.auth.crud_auth as crud_auth
from app.config.config import get_settings
from app.database.get_db import SessionLocal, get_db
from app.utils.Exceptions.exceptions import (
    Incorrect_username_or_password,
    Permission_Exception,
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(
        plain_password.encode('utf-8'), hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


def authenticate(
    email: str,
    password: str,
    db: SessionLocal = Depends(get_db),
) -> dict | bool:
    """
    Autentica um usuário com base em seu email e senha.

    Args:
        email (str): O email do usuário.
        password (str): A senha do usuário.
        db (SessionLocal, opcional): A sessão do banco de dados. Padrão é Depends(get_db).

    Returns:
        dict: Um dicionário contendo o usuário autenticado e suas permissões.
        False: Se o usuário não for encontrado ou a senha estiver incorreta.
    """
    # Obtém o usuário pelo email
    user = crud_auth.get_user_by_email(db=db, email_user=email)
    # Verifica se o usuário existe e se a senha está correta
    if not user:
        raise Incorrect_username_or_password()
    if not verify_password(password, user.senha):
        raise Incorrect_username_or_password()
    # Obtém as permissões do usuário
    permissions = crud_auth.get_user_permissions(db=db, user_id=user.id)
    if permissions is None:
        raise Permission_Exception()
    return {'user': user, 'permissions': permissions}


def create_access_token(*, data: dict, expires_delta: timedelta | None = None):
    """
    Cria um token de acesso JWT.

    Args:
        data (dict): Um dicionário contendo os dados que serão incluídos no token.
        expires_delta (timedelta, optional): A quantidade de tempo até o token expirar.
            Se None, o token expirará após 15 minutos.

    Returns:
        str: O token de acesso JWT codificado.
    """
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
