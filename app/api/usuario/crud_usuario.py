from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

import app.config.auth as auth
from app.api.reserva.reserva_model import Reservation
from app.api.usuario.usuario_model import Usuario
from app.api.usuario.usuario_schemas import UsuarioCreate
from app.database.get_db import get_db
from app.utils.Exceptions.exceptions import ObjectNotFoundException

Session = Annotated[Session, Depends(get_db)]


def get_user_by_id(user_id: int, db: Session):
    """
    Obtém um usuário pelo seu ID.

    Args:
        user_id (int): ID do usuário.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        Usuario: O usuário correspondente ao ID especificado, ou None se não for encontrado.

    Raises:
        HTTPException: Exceção HTTP com código 404 se o usuário não for encontrado.
    """
    user = db.get(Usuario, user_id)
    if not user:
        raise ObjectNotFoundException('User', user_id)
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    """
    Retorna uma lista de usuários a partir do banco de dados.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    skip (int): Quantidade de usuários a serem ignorados.
    limit (int): Quantidade máxima de usuários a serem retornados.

    Retorna:
    list[Usuario]: Lista de usuários.
    """
    return db.query(Usuario).offset(skip).limit(limit).all()


def get_users_count(db: Session):
    """
    Retorna a quantidade de usuários cadastrados no banco de dados.
    """
    user = db.query(Usuario).count()
    return user


def create_user(db: Session, user: UsuarioCreate):
    """
    Cria um novo usuário no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        user (UsuarioCreate): Os dados do usuário a serem criados.

    Returns:
        Usuario: O usuário criado.
    """
    user_dict = user.model_dump()
    if 'tipo_id' not in user_dict or user_dict['tipo_id'] is None:
        user_dict['tipo_id'] = 2

    db_user = Usuario(**user_dict)
    db_user.senha = auth.get_password_hash(db_user.senha)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_reservas(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[Reservation]:
    """
    Retorna uma lista de reservas de um usuário a partir do banco de dados.

    Args:
    db (Session): Sessão do banco de dados.
    user_id (int): ID do usuário cujas reservas serão retornadas.
    skip (int): Quantidade de reservas a serem ignorados.
    limit (int): Quantidade máxima de reservas a serem retornados.

    Retorna:
    list[reservas]: Lista de reservas do usuário.
    """
    reservas = (
        db.query(Reservation)
        .filter(Reservation.usuario_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return reservas


def update_user_password(db: Session, user: Usuario, new_password: str):
    """
    Atualiza a senha de um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user (Usuario): O usuário cuja senha será atualizada.
        new_password (str): A nova senha do usuário.
    """
    user.senha = auth.get_password_hash(new_password)
    db.commit()


def delete_user(db: Session, user: Usuario):
    """
    Deleta um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user (Usuario): O usuário a ser deletado.
    """
    db.delete(user)
    db.commit()


def delete_user_by_id(
    user_id: int,
    db: Session,
):
    """
    Deleta um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): O ID do usuário a ser deletado.
    """
    try:
        user = get_user_by_id(user_id, db)
    except ObjectNotFoundException:
        raise
    else:
        db.delete(user)
        db.commit()


def update_user(user_id: int, usuario: UsuarioCreate, db: Session):
    """
    Atualiza os detalhes de um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID do usuário a ser atualizado.
        user_update (UsuarioCreate): Os novos detalhes do usuário.

    Returns:
        Usuario: O usuário atualizado ou None se o usuário não for encontrado.
    """
    try:
        user = get_user_by_id(user_id, db)
    except ObjectNotFoundException:
        raise
    else:
        for dado, valor in usuario.model_dump().items():
            setattr(user, dado, valor)
        user.senha = auth.get_password_hash(usuario.senha)
        db.commit()
        db.refresh(user)
        return user
