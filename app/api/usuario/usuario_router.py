from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.api.auth.crud_auth as crud_auth
import app.api.usuario.crud_usuario as crud_usuario
from app.api.reserva.reserva_schema import ReservationList
from app.api.usuario.usuario_model import Usuario
from app.api.usuario.usuario_schemas import UsuarioCreate, UsuarioList
from app.config.auth import verify_password
from app.database.get_db import get_db
from app.Exceptions.exceptions import (
    email_ja_registrado_exception,
    reserva_nao_encontrada_exception,
    sem_permissao_exception,
    senha_antiga_incorreta_exception,
    senha_vazia_exception,
    user_not_found_exception,
)

router_usuario = APIRouter()

Session = Annotated[Session, Depends(get_db)]
Current_User = Annotated[Usuario, Depends(crud_usuario.get_current_user)]


@router_usuario.post('/usuarios')
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
    db_user = crud_auth.get_user_by_email(db=db, email_user=usuario.email)
    if db_user:
        raise email_ja_registrado_exception()
    return crud_usuario.create_user(db=db, user=usuario)


# FIXME: aparentimente impossivel manter essa rota privada pois o usuario não tem como se autenticar sem ter um usuario criado ai não tem como testar o if user_not_found_exception junto com o current_user os dois não da pra testar junto mas não faria sentido a listagem retornar user_not_found_exception ne?
@router_usuario.get('/usuarios', response_model=UsuarioList)
def read_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    # current_user: Type = Depends(crud_usuario.get_current_user),
):
    """
    Retorna uma lista de usuários com paginação.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    skip (int): Quantidade de registros a serem ignorados.
    limit (int): Quantidade máxima de registros a serem retornados.

    Retorna:
    dict: Dicionário contendo a lista de usuários.
    """
    # if not crud_usuario.is_admin(current_user.id, db):
    #     raise sem_permissao_exception()
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


# TODO: talvez seja melhor essa rota ser privada somente para adm não?
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

    if current_user.id != user_id and not crud_usuario.is_admin(
        current_user.id, db
    ):
        raise sem_permissao_exception()

    return db_user


# TODO: Refatorar esta rota para não precisar pegar o id do usuario é sim o usuario autenticado muito melhor...(na vez de usar o id usar o current_user: Type = Depends(crud_usuario.get_current_user) já temos algumas rotas que fazem isso mas não sei se aqui faria sentido sei la [@router_reserva.get('/usuario/reservas') usa veja se faz sentido])
@router_usuario.put('/usuarios/{user_id}')
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
    if current_user.id != user_id and not crud_usuario.is_admin(
        current_user.id, db
    ):
        raise sem_permissao_exception()

    user = crud_usuario.update_user(user_id, usuario, db)

    if user is None:
        raise user_not_found_exception()

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
    reservations = crud_usuario.get_user_reservas(db, current_user.id)
    if reservations is None:
        raise reserva_nao_encontrada_exception()
    return {'Reservation': reservations}


@router_usuario.put('/usuario/update_senha')
def update_senha(
    new_password: str,
    old_password: str,
    db: Session,
    current_user: Current_User,
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


# TODO: se eu for adicionar essas verificações todos os testes que utilizam essa rota vão quebrar é eu terei que refatorar fora que sempre terei que levar o id do usuario pra lá e pra ka
# def update_senha(
#     user_id: int,
#     new_password: str,
#     old_password: str,
#     current_user: Type = Depends(crud_usuario.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """
#     Atualiza a senha do usuário.

#     Args:
#         user_id (int): ID do usuário cuja senha será atualizada.
#         new_password (str): A nova senha para ser definida.
#         old_password (str): A senha antiga para autenticação.
#         current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
#         db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

#     Returns:
#         dict: Um dicionário indicando que a senha foi atualizada com sucesso.

#     Raises:
#         HTTPException(401): Se a senha antiga fornecida não corresponder à senha atual do usuário.
#         HTTPException(400): Se a nova senha for vazia.
#         HTTPException(404): Se o usuário não for encontrado.
#         HTTPException(403): Se o usuário atual não tem permissão para atualizar a senha do usuário especificado.
#     """
#     if crud_usuario.get_user_by_id(user_id, db) is None:
#         raise user_not_found_exception()
#     if current_user.id != user_id and not crud_usuario.is_admin(
#         current_user.id, db
#     ):
#         raise sem_permissao_exception()
#     if not verify_password(old_password, current_user.senha):
#         raise senha_antiga_incorreta_exception()
#     if not new_password:
#         raise senha_vazia_exception()
#     crud_usuario.update_user_password(db, current_user, new_password)
#     return {'detail': 'Senha atualizada com sucesso'}


@router_usuario.delete('/usuario/delete')
def delete(
    db: Session,
    current_user: Current_User,
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
    elif current_user.id == user_id or crud_usuario.is_admin(
        current_user.id, db
    ):
        crud_usuario.delete_user_by_id(user_id, db)
        return {'detail': 'Usuário deletado com sucesso'}
    else:
        raise sem_permissao_exception()
