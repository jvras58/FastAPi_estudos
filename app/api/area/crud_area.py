from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.area.area_model import Area
from app.api.area.area_schema import AreaCreate
from app.database.get_db import get_db
from app.utils.Exceptions.exceptions import (
    ObjectAlreadyExistException,
    ObjectNotFoundException,
)

Session = Annotated[Session, Depends(get_db)]


def get_areas(db: Session, skip: int = 0, limit: int = 100) -> list[Area]:
    """
    Retorna uma lista de areas a partir do banco de dados.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    skip (int): Quantidade de areas a serem ignorados.
    limit (int): Quantidade máxima de areas a serem retornados.

    Retorna:
    list[areas]: Lista de areas.
    """
    return db.query(Area).offset(skip).limit(limit).all()


# TODO: TALVEZ ESSA SEJA UMA DAS QUE NÃO PRECISE DE UMA EXCEPTION
def get_area_by_name(nome: str, db: Session):
    """
    Obtém uma área pelo seu nome.

    Args:
        nome (str): O nome da área a ser obtida.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area: A área encontrada com o nome correspondente, ou None se não for encontrada.
    """
    area = db.query(Area).filter(Area.nome == nome).first()
    if not area:
        raise ObjectNotFoundException('Area', nome)
    return area


def create_area(db: Session, area: AreaCreate):
    """
    Cria uma nova área no banco de dados.

    Verifica se o usuário associado à área existe no banco de dados e é um administrador.
    Verifica se a área já existe pelo nome.

    Args:
        db (Session): A sessão do banco de dados para consulta.
        area (AreaCreate): Os dados para criar a nova área.

    Returns:
        Area: A área recém-criada.

    Raises:
        HTTPException: Se o usuário não for encontrado, não for um administrador ou se a área já existir.
    """
    try:
        get_area_by_name(area.nome, db)
        raise ObjectAlreadyExistException('Area', area.nome)
    except ObjectNotFoundException:
        db_area = Area(**area.model_dump())
        db.add(db_area)
        db.commit()
        db.refresh(db_area)

    return db_area


def get_area_by_id(area_id: int, db: Session):
    """
    Obtém uma área pelo seu ID.

    Args:
        area_id (int): ID da área.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        Area: A área correspondente ao ID especificado.

    Raises:
        HTTPException: Exceção HTTP com código 404 se a área não for encontrada.
    """
    instance = db.get(Area, area_id)
    if not instance:
        raise ObjectNotFoundException('Area', area_id)
    return instance


def update_area(area_id: int, area: AreaCreate, db: Session):
    """
    Atualiza os detalhes de uma área.

    Args:
        db (Session): Sessão do banco de dados.
        area_id (int): ID da área a ser atualizada.
        area (AreaCreate): Os novos detalhes da área.

    Returns:
        Area: a área atualizada.
    """
    try:
        db_area = get_area_by_id(area_id, db)
    except ObjectNotFoundException:
        raise
    else:
        for dado, valor in area.model_dump().items():
            setattr(db_area, dado, valor)
        db.commit()
        db.refresh(db_area)
        return db_area


def delete_area(area_id: int, db: Session):
    """
    Deleta uma área existente.

    Args:
        area_id (int): ID da área a ser deletada.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        bool: Indica se a área foi deletada com sucesso.
    """
    try:

        db_area = get_area_by_id(area_id, db)
    except ObjectNotFoundException:
        raise
    else:
        db.delete(db_area)
        db.commit()
