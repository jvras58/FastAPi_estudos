from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends  # , HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.auth.auth_schema import Token
from app.api.auth.crud_auth import get_current_user
from app.api.usuario.usuario_model import Usuario
from app.config.auth import authenticate, create_access_token
from app.config.config import get_settings
from app.database.get_db import get_db

# from app.utils.Exceptions.exceptions import IncorrectCredentialException

router_auth = APIRouter()

Session = Annotated[Session, Depends(get_db)]
Current_User = Annotated[Usuario, Depends(get_current_user)]
form_data = Annotated[OAuth2PasswordRequestForm, Depends()]


@router_auth.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: form_data,
    db: Session,
):
    """
    Gera um token de acesso para autenticação de usuário.

    Args:
        form_data (OAuth2PasswordRequestForm): Os dados de formulário contendo email e senha.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Token: O token de acesso gerado.

    Raises:
        HTTPException(401): Se o nome de usuário ou a senha forem incorretos.
    """

    auth_result = authenticate(
        db=db, email=form_data.username, password=form_data.password
    )
    access_token_expires = timedelta(
        minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={
            'sub': auth_result['user'].email,
            'permissions': auth_result['permissions'],
        },
        expires_delta=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router_auth.post('/refresh_token', response_model=Token)
def refresh_access_token(
    current_user: dict = Depends(get_current_user),
):
    new_access_token = create_access_token(
        data={'sub': current_user['user'].email}
    )

    return {'access_token': new_access_token, 'token_type': 'bearer'}
