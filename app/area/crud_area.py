from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.area.area_model import Area
from app.area.area_schema import AreaCreate
from app.usuario.crud_usuario import get_current_admin_user, get_current_user, is_admin
from app.usuario.usuario_model import Usuario
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


def create_area(db: Session, area: AreaCreate, 
                #current_user: Usuario = Depends(get_current_admin_user)
                ):
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
    # Verifica se o usuario autenticado é do tipo adm
    # por que não ta pegando ?? AttributeError: 'Depends' object has no attribute 'id' no current_adm eu consigo pegar o id mas aqui não...
    # if  current_user.id != 1:
    #     raise HTTPException(
    #         status_code=403,
    #         detail='O usuário autenticado não é um administrador.'
    #     )
    
    # Verifica se a área já existe pelo nome
    area_exist = get_area_by_name(area.nome, db)
    if area_exist is not None:
        raise HTTPException(status_code=400, detail='Área já existe')

    db_area = Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

# FIXME: ESSE def NÃO TA BEM COM UM PROBLEMA KK (TIPO ELA TA PEGANDO MAS NO RESPONSE BODY DEPOIS DO EXECUTE ELA NÃO MOSTRA O QUE FOI MUDADO MOSTRA UM {}
# def update_area(area_id: int, area: AreaCreate, db: Session = Depends(get_db)):
#     """
#     Atualiza uma área existente.

#     Args:
#         area_id (int): ID da área a ser atualizada.
#         area (AreaCreate): Novas informações para a área.
#         db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

#     Raises:
#         HTTPException: Retorna um erro HTTP 404 se a área não for encontrada.

#     Returns:
#         Area: A área atualizada.
#     """
#     db_area = get_area_by_id(area_id, db)
#     if not db_area:
#         raise HTTPException(status_code=404, detail='Area not found')
#     update_data = area.model_dump()
#     db_area.__dict__.update(
#         update_data
#     )  # Atualiza os atributos com os dados de update_data que vem do schema de area
#     db.commit()
#     return db_area

# CHECKING : CHECAR SE ESSA FUNÇÃO ESTA FUNCIONANDO CORRETAMENTE É APRESENTANDO OS DADO NO JSON DO SWEGGER DO FASTAPI (ERRO DA FUNÇÃO ACIMA)
def update_area(area_id: int, area: AreaCreate, db: Session = Depends(get_db)):
    """
    Atualiza os detalhes de um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID do usuário a ser atualizado.
        user_update (UsuarioCreate): Os novos detalhes do usuário.

    Returns:
        Usuario: O usuário atualizado.
    """
    db_area = get_area_by_id(area_id, db)
    if not db_area:
        raise HTTPException(status_code=404, detail='Area not found')
    # itens é um método de dicionário que retorna uma lista de tuplas, onde cada tupla contém um par chave-valor(no nosso caso dado-valor[ex: {'nome': 'Novo Nome'}]) do dicionário.
    for dado, valor in area.model_dump().items():
        # O setattr é uma função embutida em Python que define o valor de um atributo de um objeto. Neste caso, estamos configurando o atributo key (que é o nome do campo) do objeto user para ter o valor value.
        setattr(area, dado, valor)
    db.commit()
    db.refresh(area)
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
