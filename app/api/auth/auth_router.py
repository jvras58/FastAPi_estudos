from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.auth.auth_schema import Token
from app.api.auth.crud_auth import get_current_user
from app.api.usuario.usuario_model import Usuario
from app.config.auth import authenticate, create_access_token
from app.config.config import get_settings
from app.database.get_db import get_db
from app.Exceptions.exceptions import Incorrect_username_or_password

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
    user = authenticate(
        db=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise Incorrect_username_or_password()
    access_token_expires = timedelta(
        minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router_auth.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: Current_User,
):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
