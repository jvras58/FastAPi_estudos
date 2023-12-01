from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.api.auth.crud_auth as crud_auth
import app.api.tipo_usuario.crud_tipo_usuario as crud_tipo_usuario
import app.api.usuario.crud_usuario as crud_usuario
from app.api.auth.crud_auth import get_current_user, verify_permission
from app.api.reserva.reserva_schema import ReservationList
from app.api.usuario.usuario_model import Usuario
from app.api.usuario.usuario_schemas import (
    UsuarioCreate,
    UsuarioList,
    UsuarioPublic,
)
from app.config.auth import verify_password
from app.config.config import get_settings
from app.database.get_db import get_db
from app.utils.Exceptions.exceptions import (
    email_ja_registrado_exception,
    reserva_nao_encontrada_exception,
    sem_permissao_exception,
    senha_antiga_incorreta_exception,
    senha_vazia_exception,
    user_not_found_exception,
    usertipo_not_found_exception,
)

router_usuario = APIRouter()

Session = Annotated[Session, Depends(get_db)]
Current_User = Annotated[Usuario, Depends(get_current_user)]


@router_usuario.get('/users/permissions')
async def read_users_me(current_user: Current_User):
    user, permissions = current_user
    return {'user': user, 'permissions': permissions}


@router_usuario.post('/usuarios', response_model=UsuarioPublic)
def create_usuario(usuario: UsuarioCreate, db: Session):
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
    if not crud_tipo_usuario.get_tipo_usuario(db, usuario.tipo_id):
        raise usertipo_not_found_exception()
    db_user = crud_auth.get_user_by_email(db=db, email_user=usuario.email)
    if db_user:
        raise email_ja_registrado_exception()
    return crud_usuario.create_user(db=db, user=usuario)


@router_usuario.get('/usuarios', response_model=UsuarioList)
def read_users(
    db: Session,
    # current_user: Current_User,
    skip: int = 0,
    limit: int = 100,
):
    """
    Retorna uma lista de usuários com paginação.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    current_user (Usuario): Usuário autenticado.
    skip (int): Quantidade de registros a serem ignorados.
    limit (int): Quantidade máxima de registros a serem retornados.

    Retorna:
    dict: Dicionário contendo a lista de usuários.
    """
    users: list[Usuario] = crud_usuario.get_users(db, skip, limit)
    if users is None:
        raise user_not_found_exception()
    return {'users': users}


@router_usuario.get('/usuarios/contagem')
def read_users_count(
    db: Session,
):
    """
    Retorna a contagem de usuários.

    Parâmetros:
    db (Session): Sessão do banco de dados.

    Retorna:
    int: A contagem de usuários.
    """
    count: int = crud_usuario.get_users_count(db)
    return {'count': count}


@router_usuario.get('/usuarios/{user_id}')
def get_user(
    user_id: int,
    db: Session,
    current_user: Current_User,
):
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
        raise user_not_found_exception()
    if current_user['user'].id != user_id and not verify_permission(
        current_user['permissions'], get_settings().ADMINISTRADOR
    ):
        raise sem_permissao_exception()

    return db_user


# TODO: Refatorar esta rota para não precisar pegar o id do usuario é sim o usuario autenticado muito melhor...(na vez de usar o id usar o current_user: Type = Depends(crud_usuario.get_current_user) já temos algumas rotas que fazem isso mas não sei se aqui faria sentido sei la [@router_reserva.get('/usuario/reservas') usa veja se faz sentido])
@router_usuario.put('/usuarios/{user_id}', response_model=UsuarioPublic)
def update_user(
    user_id: int,
    usuario: UsuarioCreate,
    db: Session,
    current_user: Current_User,
):
    """Atualiza um usuário pelo seu ID.

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
    if current_user['user'].id != user_id and not verify_permission(
        current_user['permissions'], get_settings().ADMINISTRADOR
    ):
        raise sem_permissao_exception()

    user = crud_usuario.update_user(user_id, usuario, db)

    if user is None:
        raise user_not_found_exception()

    return user


# CHECKING: Verificar se esta rota vale a pena manter ou se é melhor usar a rota de cima
@router_usuario.put('/usuarios', response_model=UsuarioPublic)
def update_user_auth(
    usuario: UsuarioCreate,
    db: Session,
    current_user: Current_User,
):
    """Atualiza o usuário atualmente autenticado.

    Args:
        usuario (UsuarioCreate): Os dados do usuário a ser atualizado.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).
        current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
    Raises:
        HTTPException: Exceção HTTP com código 404 se o usuário não for encontrado.

    Returns:
        Usuario: O usuário com informações atualizadas.
    """
    user_id = current_user['user'].id

    user = crud_usuario.update_user(user_id, usuario, db)
    return user


@router_usuario.get('/list/reservas', response_model=ReservationList)
def get_user_reservations(
    db: Session,
    current_user: Current_User,
):
    """
    Obtém as reservas do usuário atualmente autenticado.

    Args:
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).
        current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).

    Returns:
        List[reservas]: Lista de reservas associadas ao usuário.
    """
    reservations = crud_usuario.get_user_reservas(db, current_user['user'].id)
    if reservations is None:
        raise reserva_nao_encontrada_exception()
    return {'Reservation': reservations}


@router_usuario.put('/usuario/update_senha')
def update_senha(
    new_password: str,
    old_password: str,
    db: Session,
    Current_User: Current_User,
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
    user = Current_User['user']
    if not verify_password(old_password, user.senha):
        raise senha_antiga_incorreta_exception()
    if not new_password:
        raise senha_vazia_exception()
    crud_usuario.update_user_password(db, user, new_password)
    return {'detail': 'Senha atualizada com sucesso'}


@router_usuario.delete('/usuario/delete')
def delete(
    db: Session,
    Current_User: Current_User,
):
    """
    Deleta o usuário atualmente autenticado.

    Args:
        current_user (dict, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Um dicionário indicando que o usuário foi deletado com sucesso.
    """
    user = Current_User['user']
    crud_usuario.delete_user(db, user)
    return {'detail': 'Usuário deletado com sucesso'}


@router_usuario.delete('/usuarios/delete/{user_id}')
def delete_user(
    user_id: int,
    db: Session,
    current_user: Current_User,
):
    """Obtém um usuário pelo seu ID.

    Args:
        user_id (int): ID do usuário.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        dict: Um dicionário indicando que o usuário foi deletado com sucesso.
    """
    if crud_usuario.get_user_by_id(user_id, db) is None:
        raise user_not_found_exception()
    elif current_user['user'].id == user_id or verify_permission(
        current_user['permissions'], get_settings().ADMINISTRADOR
    ):
        crud_usuario.delete_user_by_id(user_id, db)
        return {'detail': 'Usuário deletado com sucesso'}
    else:
        raise sem_permissao_exception()
