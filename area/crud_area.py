from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from area.area_model import Area
from area.area_schema import AreaCreate

def get_area_by_id(area_id: str, db: Session = Depends(get_db)):
    """
    Obtém uma área pelo seu ID.

    Args:
        area_id (str): ID da área.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        Area: A área correspondente ao ID especificado.

    Raises:
        HTTPException: Exceção HTTP com código 404 se a área não for encontrada.
    """
    return db.query(Area).filter(Area.id == area_id).first()


def get_available_areas(db: Session = Depends(get_db)):
    """
    Obtém todas as áreas disponíveis.

    Args:
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        List[Area]: Uma lista de todas as áreas disponíveis.
    """
    return db.query(Area).filter(Area.disponivel == True).all()


def create_area(db: Session, area: AreaCreate):
    """
    Cria uma nova área.

    Args:
        db (Session): Sessão do banco de dados.
        area (AreaCreate): Informações da nova área.

    Raises:
        HTTPException: Retorna um erro HTTP 400 se a área já existir.

    Returns:
        Area: A nova área criada.
    """
    db_area = db.query(Area).filter(Area.nome == area.nome).first()
    if db_area:
        raise HTTPException(status_code=400, detail="Area already exists")
    db_area = Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


def update_area(area_id: str, area: AreaCreate, db: Session = Depends(get_db)):
    """
    Atualiza uma área existente.

    Args:
        area_id (str): ID da área a ser atualizada.
        area (AreaCreate): Novas informações para a área.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Raises:
        HTTPException: Retorna um erro HTTP 404 se a área não for encontrada.

    Returns:
        Area: A área atualizada.
    """
    db_area = get_area_by_id(area_id, db)
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    for key, value in area.model_dump().items():
        setattr(db_area, key, value)
    db.commit()
    return db_area

def delete_area(area_id: str, db: Session = Depends(get_db)):
    """
    Deleta uma área existente.

    Args:
        area_id (str): ID da área a ser deletada.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Raises:
        HTTPException: Retorna um erro HTTP 404 se a área não for encontrada.
    """
    db_area = get_area_by_id(area_id, db)
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    db.delete(db_area)
    db.commit()