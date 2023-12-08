from functools import lru_cache
from typing import Annotated

from cachetools import TTLCache
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.usuario.usuario_model import Usuario
from app.config.config import get_settings
from app.database.get_db import get_db
from app.utils.Exceptions.exceptions import (
    CredentialsException,
    UserNotFoundException,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

Session = Annotated[Session, Depends(get_db)]
oauth2 = Annotated[str, Depends(oauth2_scheme)]

user_cache = TTLCache(maxsize=100, ttl=300)


def verify_permission(user_permissions: list[str], required_permission: str):
    """
    Verifica se um usuário tem a permissão necessária.

    Args:
        user_permissions (list[str]): A lista de permissões atribuídas ao usuário.
        required_permission (str): A permissão a ser verificada.

    Returns:
        bool: True se o usuário tiver a permissão necessária; False caso contrário.
    """
    if required_permission in user_permissions:
        return True
    else:
        return False


def get_user_by_email(email_user: str, db: Session):
    """
    Obtém um usuário pelo endereço de e-mail.

    Args:
        email_user (str): O endereço de e-mail do usuário a ser obtido.
        db (SessionLocal, optional): Uma sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        Usuario: O usuário correspondente ao endereço de e-mail, ou None se não for encontrado.
    """
    return db.query(Usuario).filter(Usuario.email == email_user).first()


@lru_cache(maxsize=100)
def get_user_permissions(user_id: int, db: Session):
    """
    Obtém as permissões de um usuário.

    Args:
        user_id (int): O ID do usuário.
        db (SessionLocal, optional): Uma sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        List[str]: Uma lista de permissões do usuário.
    """
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise UserNotFoundException()
    # Retorna o tipo de usuário como uma permissão
    return [user.tipo.tipo]


def decode_jwt(token: str):
    """
    Decodifica um token JWT e retorna o payload.

    Args:
        token (str): O token JWT a ser decodificado.

    Returns:
        dict: O payload decodificado.
    """
    try:
        # Decodifica o token JWT
        # print(f'Token: {token}')  # Imprime o token
        payload = jwt.decode(
            token,
            get_settings().SECRET_KEY,
            algorithms=get_settings().ALGORITHM,
        )
        return payload
    except JWTError:
        raise CredentialsException()


def get_user_and_permissions(
    email: str, payload: dict, db: Session
) -> tuple[Usuario, list[str]]:
    """
    Obtém o usuário e as permissões com base no email fornecido.

    Args:
        email (str): O email do usuário.
        payload (dict): O payload contendo as permissões do usuário.
        db (Session): A sessão do banco de dados.

    Returns:
        tuple: Uma tupla contendo o usuário e as permissões.
    """
    if email not in user_cache:
        user = get_user_by_email(db=db, email_user=email)
        if user is None:
            raise CredentialsException()
        user_cache[email] = user
        # print('Usuário adicionado ao cache:', user)
        permissions = user_cache[email] = payload.get('permissions', [])
        # print('Permissões do user adicionadas ao cache:', permissions)
    else:
        user = user_cache[email]
        # print('Usuário obtido do cache:', user)
        permissions = user_cache[email]
        # print('Permissões do user obtidas do cache:', permissions)
        user = get_user_by_email(db=db, email_user=email)
    return user, permissions


async def get_current_user(token: oauth2, db: Session):
    """
    Retorna o usuário atual com base no token fornecido.

    Args:
        token (oauth2): O token de autenticação.
        db (Session): A sessão do banco de dados.
    Returns:
        dict: um dicionario contendo o usuario e as permissoes
    """
    payload = decode_jwt(token)
    # Obtem o email do usuário a partir do payload do token
    # print(f'Payload: {payload}')  # Imprime o payload decodificado
    email = payload.get('sub')
    if email is None:
        raise CredentialsException()

    user, permissions = get_user_and_permissions(email, payload, db)
    return {'user': user, 'permissions': permissions}
