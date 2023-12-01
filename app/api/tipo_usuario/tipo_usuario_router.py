from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.api.tipo_usuario.crud_tipo_usuario as crud_tipo_user
from app.api.tipo_usuario.tipo_usuario_schemas import TipoList, TipoUserCreate
from app.database.get_db import get_db

router_tipo_usuario = APIRouter()

Session = Annotated[Session, Depends(get_db)]


@router_tipo_usuario.post('/tipos_usuario')
def create_tipo_usuario(tipo_usuario: TipoUserCreate, db: Session):
    """
    Cria um novo tipo de usuário.

    Args:
        tipo_usuario (TipoUsuarioCreate): Os dados do novo tipo de usuário a ser criado.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        TipoUser: O objeto do tipo de usuário criado.
    """
    exist_tipo_usuario = crud_tipo_user.get_tipo_usuario_by_name(
        db=db, tipo=tipo_usuario.tipo
    )
    if exist_tipo_usuario:
        raise HTTPException(
            status_code=400, detail='Tipo de usuário já existe'
        )
    return crud_tipo_user.create_tipo_usuario(db=db, tipo_usuario=tipo_usuario)


@router_tipo_usuario.get('/tipos_usuario', response_model=TipoList)
def read_tipo_users(
    db: Session,
    # current_user: Current_User,
    skip: int = 0,
    limit: int = 100,
):
    """
    Retorna uma lista de tipos de usuarios com paginação.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    current_user (Usuario): Usuário autenticado.
    skip (int): Quantidade de registros a serem ignorados.
    limit (int): Quantidade máxima de registros a serem retornados.

    Retorna:
    dict: Dicionário contendo a lista de tipos.
    """
    tipos: list[TipoList] = crud_tipo_user.get_tipo_usuarios(db, skip, limit)
    if tipos is None:
        raise HTTPException(
            status_code=404, detail='Tipo de usuário não encontrado'
        )
    return {'tipos': tipos}


@router_tipo_usuario.put('/tipos_usuario/{tipo_usuario_id}')
def update_tipo_usuario(
    tipo_usuario_id: int, tipo_usuario: TipoUserCreate, db: Session
):
    """
    Atualiza um tipo de usuário existente.

    Args:
        tipo_usuario_id (int): O ID do tipo de usuário a ser atualizado.
        tipo_usuario (TipoUserCreate): Os novos dados do tipo de usuário.

    Returns:
        TipoUser: O objeto do tipo de usuário atualizado.
    """
    db_tipo_usuario = crud_tipo_user.get_tipo_usuario(
        db=db, tipo_usuario_id=tipo_usuario_id
    )
    if db_tipo_usuario is None:
        raise HTTPException(
            status_code=404, detail='Tipo de usuário não encontrado'
        )
    return crud_tipo_user.update_tipo_usuario(
        db=db, tipo_usuario_id=tipo_usuario_id, tipo_usuario=tipo_usuario
    )


@router_tipo_usuario.delete('/tipos_usuario/{tipo_usuario_id}')
def delete_tipo_usuario(tipo_usuario_id: int, db: Session):
    """
    Exclui um tipo de usuário existente.

    Args:
        tipo_usuario_id (int): O ID do tipo de usuário a ser excluído.

    Returns:
        None
    """
    db_tipo_usuario = crud_tipo_user.get_tipo_usuario(
        db=db, tipo_usuario_id=tipo_usuario_id
    )
    if db_tipo_usuario is None:
        raise HTTPException(
            status_code=404, detail='Tipo de usuário não encontrado'
        )
    tipos_usuarios = crud_tipo_user.get_tipo_usuarios(db, skip=0, limit=100)
    tipos_ids = [tipo.id for tipo in tipos_usuarios]
    tipos_ids.remove(tipo_usuario_id)
    new_tipo_usuario_id = tipos_ids[0] if tipos_ids else None
    crud_tipo_user.reassign_users_and_delete_tipo_usuario(
        db=db,
        tipo_usuario_id=tipo_usuario_id,
        new_tipo_usuario_id=new_tipo_usuario_id,
    )
    return {
        'detail': 'Tipo de usuário excluído com sucesso usuarios reatribuidos ao tipo de usuário padrão'
    }
