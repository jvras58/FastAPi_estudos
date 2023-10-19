from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from area.area_model import Area
from area.area_schema import AreaCreate
from user.user_model import Usuario

# TODO: MODIFICAÇÕES COM BASE NO PROJETO BASE  
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

# TODO: MODIFICAÇÕES COM BASE NO PROJETO BASE 
def get_all(db: Session = Depends(get_db)):
    """
    Obtém todas as áreas no banco de dados.

    Args:
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Area]: Uma lista de todas as áreas.
    """
    return db.query(Area).all()

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

# TODO: MODIFICAÇÕES COM BASE NO PROJETO BASE                                                                                                                                                                      #tipo de usuario...
def create_area(db: Session, area: AreaCreate):
    """
    Cria uma nova área no banco de dados.

    Args:
        db (Session): Uma sessão do banco de dados.
        area (AreaCreate): Os dados da nova área.

    Returns:
        Area: A nova área criada.
    """
    # Verifica se o usuário associado à área existe no banco de dados (é se o tipo é de admiro falta definir isso na tabela de usuario)
    user = db.query(Usuario).filter(Usuario.id == area.usuario_id, Usuario.tipo == 0).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user or user type")

    # Verifica se a área já existe pelo nome
    db_area = db.query(Area).filter(Area.nome == area.nome).first()
    if db_area:
        raise HTTPException(status_code=400, detail="Area already exists")

    # Cria a nova área associando o ID do usuário
    db_area = Area(**area.model_dump(), usuario_id=area.usuario_id)

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

# TODO: MODIFICAÇÕES/ATUALIZAÇÕES COM BASE NO PROJETO BASE
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

# EXCLUDEME: VERSÃO ANTIGA
# def delete_area_update(area_id: str, db: Session = Depends(get_db)):
#     """
#     Define a disponibilidade de uma área como `False`, em vez de excluir completamente do banco de dados.

#     Args:
#         area_id (str): O ID da área a ser atualizada.
#         db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

#     Raises:
#         HTTPException: Retorna um erro HTTP 404 se a área não for encontrada.
#     """
#     db_area = get_area_by_id(area_id, db)
#     if not db_area:
#         raise HTTPException(status_code=404, detail="Area not found")
#     db_area.disponivel = False
#     db.commit()