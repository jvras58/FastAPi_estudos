from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.usuario.crud_usuario import is_admin
from database.get_db import SessionLocal, get_db
from app.area.area_model import Area
from app.area.area_schema import AreaCreate



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

# CRUD DESATIVADO
# FIXME: FOI RETIRADO ESSA COLUNA CHAMADA DISPONIVEL VERIFICAR OQ DA PRA FAZER COM ESSA ROTA
# def get_available_areas(db: Session = Depends(get_db)):
#     """
#     Obtém todas as áreas disponíveis.

#     Args:
#         db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

#     Returns:
#         List[Area]: Uma lista de todas as áreas disponíveis.
#     """
#     return db.query(Area).filter(Area.disponivel == True).all()

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
    # Verifica se o usuário associado à área existe no banco de dados é administrador
    if not is_admin(area.usuario_id, db):
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou não é administrador")

    # Verifica se a área já existe pelo nome
    area_exist = get_area_by_name(area.nome, db)
    if area_exist is not None:
        raise HTTPException(status_code=400, detail="Área já existe")

    # Criar a nova área associando o ID do usuário
    db_area = Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

# FIXME: ESSE CRUD NÃO TA BEM COM UM PROBLEMA KK (TIPO ELA TA PEGANDO MAS NO RESPONSE BODY DEPOIS DO EXECUTE ELA NÃO MOSTRA O QUE FOI MUDADO MOSTRA UM {} SÓ ENFIM COISAS PRA VER DEPOIS AMÉM?)
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
    update_data = area.model_dump()
    db_area.__dict__.update(update_data)  # Atualiza os atributos com os dados de update_data que vem do schema de area
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
