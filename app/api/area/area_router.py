from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.api.area.crud_area as crud_area
from app.api.area.area_model import Area
from app.api.area.area_schema import AreaCreate, AreaList, AreaPublic
from app.api.auth.crud_auth import get_current_user, verify_permission
from app.api.usuario.usuario_model import Usuario
from app.config.config import get_settings
from app.database.get_db import get_db
from app.utils.Exceptions.exceptions import (
    ObjectAlreadyExistException,
    ObjectNotFoundException,
    sem_permissao_exception,
)

router_area = APIRouter()

Session = Annotated[Session, Depends(get_db)]
Current_User = Annotated[Usuario, Depends(get_current_user)]


@router_area.post('/areas', response_model=AreaPublic)
def create_area(
    area: AreaCreate,
    Current_User: Current_User,
    db: Session,
):
    """
    Criar uma nova área.

    Args:
        area (AreaCreate): Os detalhes da nova área.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area: A área criada.
    """
    if not verify_permission(
        Current_User['permissions'], get_settings().ADMINISTRADOR
    ):
        raise sem_permissao_exception()
    try:
        return crud_area.create_area(db=db, area=area)
    except ObjectAlreadyExistException as ex:
        raise HTTPException(status_code=409, detail=ex.args[0]) from ex


@router_area.get('/areas', response_model=AreaList)
def read_areas(db: Session, skip: int = 0, limit: int = 100):
    """
    Retorna uma lista de areas com paginação.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    skip (int): Quantidade de registros a serem ignorados.
    limit (int): Quantidade máxima de registros a serem retornados.

    Retorna:
    dict: Dicionário contendo a lista de areas.
    """
    areas: list[Area] = crud_area.get_areas(db, skip, limit)
    return {'areas': areas}


@router_area.get('/areas/nome/{nome}')
def get_area_by_name(nome: str, db: Session):
    """
    Visualiza a area pelo nome.

    Args:
        nome (str): Os detalhes da nova área.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area:  A área encontrada com o nome correspondente, ou None se não for encontrada.
    """
    try:
        db_area = crud_area.get_area_by_name(nome, db)
        return db_area
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex


@router_area.get('/areas/{area_id}')
def get_area(
    area_id: int,
    Current_User: Current_User,
    db: Session,
):
    """
    Obter uma área pelo seu ID.

    Args:
        area_id (int): O ID da área a ser obtida.
        current_user (Current_User): O usuário atual.
        db (Session, optional): Uma sessão do banco de dados obtida via Depends(get_db).

    Returns:
        Area: Os detalhes da área encontrada.
    """
    if not verify_permission(
        Current_User['permissions'], get_settings().ADMINISTRADOR
    ):
        raise sem_permissao_exception()
    try:
        return crud_area.get_area_by_id(area_id, db)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex


@router_area.put('/areas/{area_id}')
def update_area(
    area_id: int,
    area: AreaCreate,
    Current_User: Current_User,
    db: Session,
):
    """
    Atualizar os detalhes de uma área.

    Args:
        area_id (int): O ID da área a ser atualizada.
        area (AreaCreate): Os novos detalhes da área.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area: Os detalhes atualizados da área.
    """
    if not verify_permission(
        Current_User['permissions'], get_settings().ADMINISTRADOR
    ):
        raise sem_permissao_exception()
    try:
        return crud_area.update_area(area_id, area, db)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex


@router_area.delete('/areas/{area_id}')
def delete_area(
    area_id: int,
    Current_User: Current_User,
    db: Session,
):
    """
    Deletar uma área.

    Args:
        area_id (int): O ID da área a ser deletada.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Uma mensagem indicando se a área foi deletada com sucesso.
    """
    if not verify_permission(
        Current_User['permissions'], get_settings().ADMINISTRADOR
    ):
        raise sem_permissao_exception()

    try:
        crud_area.delete_area(area_id, db)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex
    return {'detail': 'Área deletada com sucesso'}
