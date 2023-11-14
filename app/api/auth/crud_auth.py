from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.usuario.usuario_model import Usuario
from app.config.config import get_settings
from app.database.get_db import get_db
from app.Exceptions.exceptions import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

Session = Annotated[Session, Depends(get_db)]
oauth2 = Annotated[str, Depends(oauth2_scheme)]


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
        Usuario: O usuário autenticado.

    Raises:
        HTTPException: Exceção HTTP com código 401 se as credenciais não puderem ser validadas.
    """
    try:
        payload = jwt.decode(
            token,
            get_settings().SECRET_KEY,
            algorithms=get_settings().ALGORITHM,
        )
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception()
    except JWTError:
        raise credentials_exception()

    user = get_user_by_email(db=db, email_user=email)
    if user is None:
        raise credentials_exception()
    return user
