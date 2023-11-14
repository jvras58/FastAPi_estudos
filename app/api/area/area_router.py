from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.api.area.crud_area as crud_area
from app.api.area.area_model import Area
from app.api.area.area_schema import AreaCreate, AreaList
from app.api.usuario.crud_usuario import get_current_admin_user
from app.api.usuario.usuario_model import Usuario
from app.database.get_db import get_db
from app.Exceptions.exceptions import area_nao_encontrada_exception

router_area = APIRouter()

Session = Annotated[Session, Depends(get_db)]
current_admin_user = Annotated[Usuario, Depends(get_current_admin_user)]


@router_area.post('/areas')
def create_area(
    area: AreaCreate,
    current_admin_user: current_admin_user,
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
    return crud_area.create_area(db=db, area=area)


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
    if areas is None:
        raise area_nao_encontrada_exception()
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
    db_area = crud_area.get_area_by_name(nome, db)
    if db_area is None:
        raise area_nao_encontrada_exception()
    return db_area


@router_area.get('/areas/{area_id}')
def get_area(
    area_id: int,
    current_admin_user: current_admin_user,
    db: Session,
):
    """
    Obter uma área pelo seu ID.

    Args:
        area_id (int): O ID da área a ser obtida.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area: Os detalhes da área encontrada.
    """
    db_area = crud_area.get_area_by_id(area_id, db)
    if db_area is None:
        raise area_nao_encontrada_exception()
    return db_area


@router_area.put('/areas/{area_id}')
def update_area(
    area_id: int,
    area: AreaCreate,
    current_admin_user: current_admin_user,
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
    updated_area = crud_area.update_area(area_id, area, db)
    if updated_area is None:
        raise area_nao_encontrada_exception()
    return crud_area.update_area(area_id, area, db)


@router_area.delete('/areas/{area_id}')
def delete_area(
    area_id: int,
    current_admin_user: current_admin_user,
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
    delete_area = crud_area.delete_area(area_id, db)
    if delete_area:
        return {'detail': 'Área deletada com sucesso'}
    else:
        raise area_nao_encontrada_exception()
