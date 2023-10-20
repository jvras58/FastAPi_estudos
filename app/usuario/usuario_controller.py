from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, Type
from database.get_db import get_db
from datetime import timedelta
from app.security.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate, create_access_token, verify_password
from fastapi import APIRouter

#user 
from app.usuario.usuario_schemas import UsuarioCreate, Token
import app.usuario.crud_usuario as crud_user

router = APIRouter()

@router.post('/usuarios')
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.

    Args:
        usuario (UsuarioCreate): Os dados do novo usuário a ser criado.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Usuario: O objeto do usuário criado.

    Raises:
        HTTPException(400): Se o email já estiver registrado no sistema.
    """
    db_user = crud_user.get_user_by_email(db = db, email_user=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=usuario)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
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
    user = authenticate(db = db, email = form_data.username, password = form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/usuario/update_senha")
def update_senha(new_password: str, old_password: str, current_user: Type = Depends(crud_user.get_current_user), db: Session = Depends(get_db)):
    """
    Atualiza a senha do usuário.

    Args:
        new_password (str): A nova senha para ser definida.
        old_password (str): A senha antiga para autenticação.
        current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Um dicionário indicando que a senha foi atualizada com sucesso.

    Raises:
        HTTPException(401): Se a senha antiga fornecida não corresponder à senha atual do usuário.
        HTTPException(400): Se a nova senha for vazia.
    """
    if not verify_password(old_password, current_user.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Senha antiga incorreta")
    if not new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nova senha não pode ser vazia")
    crud_user.update_user_password(db, current_user, new_password)
    return {"detail": "Senha atualizada com sucesso"}

@router.delete("/usuario/delete")
def delete(current_user = Depends(crud_user.get_current_user), db: Session = Depends(get_db)):
    """
    Deleta o usuário atualmente autenticado.

    Args:
        current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Um dicionário indicando que o usuário foi deletado com sucesso.
    """
    crud_user.delete_user(db, current_user)
    return {"detail": "Usuário deletado com sucesso"}