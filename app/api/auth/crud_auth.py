from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.usuario.usuario_model import Usuario
from app.config.config import get_settings
from app.database.get_db import get_db
from app.utils.Exceptions.exceptions import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

Session = Annotated[Session, Depends(get_db)]
oauth2 = Annotated[str, Depends(oauth2_scheme)]


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
        return []
    # Retorna o tipo de usuário como uma permissão
    return [user.tipo.tipo]


async def get_current_user(
    token: oauth2,
    db: Session,
):
    """
    Obtém o usuário atual a partir do token de autenticação.

    Args:
        token (str): Token de autenticação.
        db (SessionLocal, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        dict: Um dicionário contendo o usuário autenticado e suas permissões.

    Raises:
        HTTPException: Exceção HTTP com código 401 se as credenciais não puderem ser validadas.
    """
    try:
        # Decodifica o token JWT
        # print(f'Token: {token}')  # Imprime o token
        payload = jwt.decode(
            token,
            get_settings().SECRET_KEY,
            algorithms=get_settings().ALGORITHM,
        )
        # Obtem o email do usuário a partir do payload do token
        # print(f'Payload: {payload}')  # Imprime o payload decodificado
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception()
        # Obtm as permissões do usuário a partir do payload do token
        permissions: list[str] = payload.get('permissions', [])
    except JWTError:
        raise credentials_exception()
    # Obtem o usuário pelo email e retornar o usuário e suas permissões
    user = get_user_by_email(db=db, email_user=email)
    if user is None:
        raise credentials_exception()

    return {'user': user, 'permissions': permissions}
