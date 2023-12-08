from sqlalchemy import func, update
from sqlalchemy.orm import Session

from app.api.tipo_usuario.tipo_usuario_model import TipoUser
from app.api.tipo_usuario.tipo_usuario_schemas import TipoUserCreate
from app.api.usuario.usuario_model import Usuario
from app.utils.Exceptions.exceptions import (
    ObjectAlreadyExistException,
    ObjectNotFoundException,
)


def get_tipo_usuario_by_name(db: Session, tipo: str):
    """
    Retorna um tipo de usuário específico pelo nome.

    Args:
        db (Session): Uma sessão do banco de dados.
        tipo_usuario_name (str): O nome do tipo de usuário.

    Returns:
        TipoUser: O objeto do tipo de usuário.
    """
    tipouser = (
        db.query(TipoUser)
        .filter(func.lower(TipoUser.tipo).ilike(func.lower(f'%{tipo}%')))
        .first()
    )
    if not tipouser:
        raise ObjectNotFoundException('Tipo de usuario', tipo)
    return tipouser


def create_tipo_usuario(db: Session, tipo_usuario: TipoUserCreate):
    """
    Cria um novo tipo de usuário.

    Args:
        tipo_usuario (TipoUsuarioCreate): Os dados do novo tipo de usuário a ser criado.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        TipoUser: O objeto do tipo de usuário criado.
    """
    try:
        get_tipo_usuario_by_name(db, tipo_usuario.tipo)
        raise ObjectAlreadyExistException('Tipo de usuario', tipo_usuario.tipo)
    except ObjectNotFoundException:
        db_tipo_usuario = TipoUser(**tipo_usuario.model_dump())
        db.add(db_tipo_usuario)
        db.commit()
        db.refresh(db_tipo_usuario)
        return db_tipo_usuario


def get_tipo_usuario(db: Session, tipo_usuario_id: int):
    """
    Retorna um tipo de usuário específico pelo ID.

    Args:
        db (Session): Uma sessão do banco de dados.
        tipo_usuario_id (int): O ID do tipo de usuário.

    Returns:
        TipoUser: O objeto do tipo de usuário.
    """

    tipo_user = db.get(TipoUser, tipo_usuario_id)
    if not tipo_user:
        raise ObjectNotFoundException('Tipo de usuario', tipo_usuario_id)
    return tipo_user


def get_tipo_usuarios(
    db: Session, skip: int = 0, limit: int = 100
) -> list[TipoUser]:
    """
    Retorna uma lista de tipos de usuario a partir do banco de dados.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    skip (int): Quantidade de usuários a serem ignorados.
    limit (int): Quantidade máxima de usuários a serem retornados.

    Retorna:
    list[TipoUser]: Lista de tipos de usuario.
    """
    return db.query(TipoUser).offset(skip).limit(limit).all()


def update_tipo_usuario(
    db: Session, tipo_usuario_id: int, tipo_usuario: TipoUserCreate
):
    """
    Atualiza um tipo de usuário existente.

    Args:
        tipo_usuario_id (int): O ID do tipo de usuário a ser atualizado.
        tipo_usuario (TipoUserCreate): Os novos dados do tipo de usuário.
        db (Session): Uma sessão do banco de dados.

    Returns:
        TipoUser: O objeto do tipo de usuário atualizado.
    """
    db_tipo_usuario = get_tipo_usuario(db, tipo_usuario_id)
    for key, value in tipo_usuario.model_dump().items():
        setattr(db_tipo_usuario, key, value)
    db.commit()
    db.refresh(db_tipo_usuario)
    return db_tipo_usuario


def reassign_users_and_delete_tipo_usuario(
    db: Session, tipo_usuario_id: int, new_tipo_usuario_id: int
):
    """
    Reatribui os usuários a um tipo de usuário diferente antes de excluir o tipo de usuário anterior.

    Args:
        tipo_usuario_id (int): O ID do tipo de usuário a ser excluído.
        new_tipo_usuario_id (int): O ID do novo tipo de usuário.

    Returns:
        None
    """
    # Atualiza o campo tipo_id dos usuários para o novo tipo de usuário
    stmt = (
        update(Usuario)
        .where(Usuario.tipo_id == tipo_usuario_id)
        .values(tipo_id=new_tipo_usuario_id)
    )
    db.execute(stmt)

    # Exclui o tipo de usuário anterior
    db_tipo_usuario = get_tipo_usuario(db, tipo_usuario_id)
    db.delete(db_tipo_usuario)
    db.commit()
