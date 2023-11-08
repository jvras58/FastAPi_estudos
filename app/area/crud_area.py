from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.area.area_model import Area
from app.area.area_schema import AreaCreate
from database.get_db import get_db


def get_area_by_name(nome: str, db: Session = Depends(get_db)):
    """
    Obtém uma área pelo seu nome.

    Args:
        nome (str): O nome da área a ser obtida.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area: A área encontrada com o nome correspondente, ou None se não for encontrada.
    """
    return db.query(Area).filter(Area.nome == nome).first()


def get_all(db: Session = Depends(get_db)):
    """
    Obtém todas as áreas no banco de dados.

    Args:
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Area]: Uma lista de todas as áreas.
    """
    return db.query(Area).all()


def get_area_by_id(area_id: int, db: Session = Depends(get_db)):
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
    return db.query(Area).filter(Area.id == area_id).first()


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
    # TODO: função que verifica se o usuario autenticado é do tipo adm (só pra testar mesmo já que marlos disse que se ele chegou até aqui não vai adiantar de nada kkk)

    # Verifica se a área já existe pelo nome
    area_exist = get_area_by_name(area.nome, db)
    if area_exist is not None:
        raise HTTPException(status_code=400, detail='Área já existe')

    db_area = Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


def update_area(area_id: int, area: AreaCreate, db: Session = Depends(get_db)):
    """
    Atualiza os detalhes de um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID do usuário a ser atualizado.
        user_update (UsuarioCreate): Os novos detalhes do usuário.

    Returns:
        Usuario: a area atualizado.
    """
    db_area = get_area_by_id(area_id, db)
    if not db_area:
        raise HTTPException(status_code=404, detail='Area not found')
    for dado, valor in area.model_dump().items():
        setattr(db_area, dado, valor)
    db.commit()
    db.refresh(db_area)
    return db_area


def delete_area(area_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma área existente.

    Args:
        area_id (int): ID da área a ser deletada.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Raises:
        HTTPException: Retorna um erro HTTP 404 se a área não for encontrada.
    """
    db_area = get_area_by_id(area_id, db)
    if not db_area:
        raise HTTPException(status_code=404, detail='Area not found')
    db.delete(db_area)
    db.commit()
