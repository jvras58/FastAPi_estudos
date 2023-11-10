from datetime import timedelta
from typing import Annotated, Type

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.usuario.crud_usuario as crud_usuario
from app.Exceptions.exceptions import (
    senha_antiga_incorreta_exception,
    senha_vazia_exception,
    user_not_found1_exception,
    user_not_found_exception,
)
from app.security.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate,
    create_access_token,
    verify_password,
)
from app.usuario.usuario_schemas import Token, UsuarioCreate
from database.get_db import get_db

router_usuario = APIRouter()


@router_usuario.post('/usuarios')
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
    db_user = crud_usuario.get_user_by_email(db=db, email_user=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail='E-mail já registrado')
    return crud_usuario.create_user(db=db, user=usuario)


@router_usuario.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router_usuario.get('/usuarios/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtém um usuário pelo seu ID.

    Args:
        user_id (int): ID do usuário.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Raises:
        HTTPException: Exceção HTTP com código 404 se o usuário não for encontrado.

    Returns:
        Usuario: O usuário correspondente ao ID especificado.
    """
    db_user = crud_usuario.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return db_user


# TODO: Refatorar esta rota para não precisar pegar o id do usuario é sim o usuario autenticado muito melhor...(na vez de usar o id usar o current_user: Type = Depends(crud_usuario.get_current_user) já temos algumas rotas que fazem isso mas não sei se aqui faria sentido sei la [@router_reserva.get('/usuario/reservas') usa veja se faz sentido])
@router_usuario.put('/usuarios/{user_id}')
def update_user(
    user_id: int,
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Type = Depends(crud_usuario.get_current_user),
):
    """Obtém um usuário pelo seu ID.

    Args:
        user_id (int): ID do usuário.
        usuario (UsuarioCreate): Os dados do usuário a ser atualizado.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).
        current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
    Raises:
        HTTPException: Exceção HTTP com código 404 se o usuário não for encontrado.

    Returns:
        Usuario: O usuário com informações atualizadas.
    """
    user = crud_usuario.update_user(user_id, usuario, db)
    if user is None:
        raise user_not_found_exception()
    return user


# TODO: Refatorar esta rota para não precisar pegar o id do usuario é sim o usuario autenticado muito melhor...(na vez de usar o id usar o current_user: Type = Depends(crud_usuario.get_current_user) já temos algumas rotas que fazem isso mas não sei se aqui faria sentido sei la [@router_reserva.get('/usuario/reservas') usa veja se faz sentido])
@router_usuario.get('/usuarios/{user_id}/reservas')
def get_user_reservations(user_id: int, db: Session = Depends(get_db)):
    """Obtém reservas associadas a uma conta pelo seu ID.

    Args:
        user_id (int): ID do usuário.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        List[reservas]: Lista de reservas associadas ao usuário.
    """
    return crud_usuario.get_user_reservations(user_id, db)


@router_usuario.put('/usuario/update_senha')
def update_senha(
    new_password: str,
    old_password: str,
    current_user: Type = Depends(crud_usuario.get_current_user),
    db: Session = Depends(get_db),
):
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
        raise senha_antiga_incorreta_exception()
    if not new_password:
        raise senha_vazia_exception()
    crud_usuario.update_user_password(db, current_user, new_password)
    return {'detail': 'Senha atualizada com sucesso'}


@router_usuario.delete('/usuario/delete')
def delete(
    current_user=Depends(crud_usuario.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Deleta o usuário atualmente autenticado.

    Args:
        current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Um dicionário indicando que o usuário foi deletado com sucesso.
    """
    crud_usuario.delete_user(db, current_user)
    return {'detail': 'Usuário deletado com sucesso'}


# TODO: melhorar o codigo para sempre perguntar se o id que esta acessando a rota é o id do usuario autenticado se sim pode prosseguir senão verificar se é adm se for ele consegue apagar se não so lamentos
@router_usuario.delete('/usuarios/delete/{user_id}')
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Type = Depends(crud_usuario.get_current_user),
):
    """Obtém um usuário pelo seu ID.

    Args:
        user_id (int): ID do usuário.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        dict: Um dicionário indicando que o usuário foi deletado com sucesso.
    """
    if not crud_usuario.get_user_by_id(user_id, db):
        raise user_not_found1_exception()
    if crud_usuario.delete_user_by_id(user_id, db):
        return {'detail': 'Usuário deletado com sucesso'}
