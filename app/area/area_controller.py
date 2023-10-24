from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.get_db import get_db
from fastapi import APIRouter

# areas
from app.area.area_schema import AreaCreate
import app.area.crud_area as crud_area

router_area = APIRouter()



@router_area.post('/areas')
def create_area(area: AreaCreate, db: Session = Depends(get_db)):
    """
    Criar uma nova área.

    Args:
        area (AreaCreate): Os detalhes da nova área.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area: A área criada.
    """  
    return crud_area.create_area(db=db, area=area)

@router_area.get('/areas')
def get_all_areas(db: Session = Depends(get_db)):
    """
    Visualiza todas as areas.

    Args:
        
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Areas: Todas as areas.
    """  
    return crud_area.get_all(db)

@router_area.get('/areas/nome/{nome}')
def get_area_by_name(nome: str, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=404, detail="Area not found")
    return db_area

# ROTA DESATIVADA
# FIXME: FOI RETIRADO ESSA COLUNA CHAMADA DISPONIVEL VERIFICAR OQ DA PRA FAZER COM ESSA ROTA
# @router_area.get('/areas/disponiveis')
# def get_areas_disponiveis(db: Session = Depends(get_db)):
#     """
#     Obter todas as áreas disponíveis.

#     Args:
#         db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

#     Returns:
#         List[Area]: Uma lista de áreas disponíveis.
#     """  
#     return crud_area.get_available_areas(db)


@router_area.get('/areas/{area_id}')
def get_area(area_id: str, db: Session = Depends(get_db)):
    """
    Obter uma área pelo seu ID.

    Args:
        area_id (str): O ID da área a ser obtida.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area: Os detalhes da área encontrada.
    """    
    db_area = crud_area.get_area_by_id(area_id, db)
    if db_area is None:
        raise HTTPException(status_code=404, detail="Area not found")
    return db_area

# FIXME: ESSA ROTA NÃO TA BEM COM UM PROBLEMA KK (TIPO ELA TA PEGANDO MAS NO RESPONSE BODY DEPOIS DO EXECUTE ELA NÃO MOSTRA O QUE FOI MUDADO MOSTRA UM {} SÓ ENFIM COISAS PRA VER DEPOIS AMÉM?)
@router_area.put('/areas/{area_id}')
def update_area(area_id: str, area: AreaCreate, db: Session = Depends(get_db)):
    """
    Atualizar os detalhes de uma área.

    Args:
        area_id (str): O ID da área a ser atualizada.
        area (AreaCreate): Os novos detalhes da área.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Area: Os detalhes atualizados da área.
    """
    return crud_area.update_area(area_id, area, db)


@router_area.delete('/areas/{area_id}')
def delete_area(area_id: str, db: Session = Depends(get_db)):
    """
    Deletar uma área.

    Args:
        area_id (str): O ID da área a ser deletada.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Uma mensagem indicando que a área foi deletada com sucesso.
    """
    crud_area.delete_area(area_id, db)
    return {"detail": "Área deletada com sucesso"}