from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Type
from database.get_db import get_db

#usuario
from user.user_schemas import UsuarioCreate, Token
import user.crud_user as crud_user
# reservas
from reserva.reserva_schema import ReservationCreate
import reserva.crud_reseva as crud_reserva
# areas
from area.area_schema import AreaCreate
import area.crud_area as crud_area

from datetime import timedelta
from security.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate, create_access_token, verify_password

# uvicorn main:app --reload  <-- inicia o servidor

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# ----------------------------------------- usuario -------------------------------------------------------#
@app.post('/usuarios')
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.

    Args:
        usuario (UsuarioCreate): Os dados do novo usuário a ser criado.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Usuario: O objeto do usuário criado.

    Raises:
        HTTPException(400): Se o email já estiver registrado no sistema.
    """
    db_user = crud_user.get_user_by_email(db = db, email_user=usuario.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=usuario)

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """
    Gera um token de acesso para autenticação de usuário.

    Args:
        form_data (OAuth2PasswordRequestForm): Os dados de formulário contendo email e senha.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Token: O token de acesso gerado.

    Raises:
        HTTPException(401): Se o nome de usuário ou a senha forem incorretos.
    """
    user = authenticate(db = db, email = form_data.username, password = form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/usuario/update_senha")
def update_senha(new_password: str, old_password: str, current_user: Type = Depends(crud_user.get_current_user), db: Session = Depends(get_db)):
    """
    Atualiza a senha do usuário.

    Args:
        new_password (str): A nova senha para ser definida.
        old_password (str): A senha antiga para autenticação.
        current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Um dicionário indicando que a senha foi atualizada com sucesso.

    Raises:
        HTTPException(401): Se a senha antiga fornecida não corresponder à senha atual do usuário.
        HTTPException(400): Se a nova senha for vazia.
    """
    if not verify_password(old_password, current_user.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Senha antiga incorreta")
    if not new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nova senha não pode ser vazia")
    crud_user.update_user_password(db, current_user, new_password)
    return {"detail": "Senha atualizada com sucesso"}

@app.delete("/usuario/delete")
def delete(current_user = Depends(crud_user.get_current_user), db: Session = Depends(get_db)):
    """
    Deleta o usuário atualmente autenticado.

    Args:
        current_user (Type, optional): O usuário atual obtido a partir do token. obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Um dicionário indicando que o usuário foi deletado com sucesso.
    """
    crud_user.delete_user(db, current_user)
    return {"detail": "Usuário deletado com sucesso"}

# ----------------------------------------- area -------------------------------------------------------#


# CENARIO: Segel entra como admiro do sistema é cria uma area(uma quadra disponivel para reserva... )
@app.post('/areas')
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


# CENARIO: segel consegue ver as areas(quadras) que estão sendo ofertadas isso o cliente tbm consegue ver 
@app.get('/areas/disponiveis')
def get_areas_disponiveis(db: Session = Depends(get_db)):
    """
    Obter todas as áreas disponíveis.

    Args:
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Area]: Uma lista de áreas disponíveis.
    """  
    return crud_area.get_available_areas(db)

# CENARIO: usuario & segell consegue pegar informações sobre a area é feedbacks de quem ja utilizou a area (talvez)
@app.get('/areas/{area_id}')
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

# CENARIO: atualizar a area (somente a segeel pode fazer isso)
@app.put('/areas/{area_id}')
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

#CENARIO: apagar area (somente a segeel pode fazer isso)
@app.delete('/areas/{area_id}')
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

# ----------------------------------------- reserva -------------------------------------------------------#
# CENARIO: USUARIO CLIENTE CRIA UMA RESERVA
# TODO: CORREÇÃO DE CONDIÇÃO PARA CRIAÇÃO DE RESERVA PARA DEFINIR SE É DISPONIVEL OU NÃO POR HORARIO
@app.post('/reservas')
def create_reserva(reserva: ReservationCreate, db: Session = Depends(get_db)):
    """
    Criar uma nova reserva.

    Args:
        reserva (ReservationCreate): Os detalhes da reserva a ser criada.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: A reserva criada.
    """
    response = crud_reserva.create_reservation(db=db, reservation=reserva)
    if response is None:
        raise HTTPException(status_code=400, detail="Horário indiponível para essa Área")
    return response


# CENARIO: USUARIO CONSEGUE VER AS RESERVAS DISPONIVEIS FEITAS POR ELE OU POSSIVEIS DE FAZER POR ELE
@app.get('/reservas/disponiveis')
def get_reservas_disponiveis(db: Session = Depends(get_db)):
    """
    Obter a lista de reservas disponíveis.

    Args:
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de reservas disponíveis.
    """
    return crud_reserva.get_available_reservations(db)

# CENARIO: VER os detalhes da reserva
@app.get('/reservas/{reservation_id}')
def get_reserva(reservation_id: str, db: Session = Depends(get_db)):
    """
    Obter os detalhes de uma reserva pelo ID.

    Args:
        reservation_id (str): O ID da reserva.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: Os detalhes da reserva.
    """
    db_reservation = crud_reserva.get_reservation_by_id(reservation_id, db)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

# CENARIO: ATUALIZAR A RESERVA (CUIDADO COM ESSE CENARIO PQ TIPO PODE HAVER CONFUSÃO UM USUARIO PODERIA AUMENTAR A RESERVA POR MOTIVOS NENHUM É ACABAR PREJUDICANDO OUTRA RESERVA JÁ QUE PODE SER POR HORARIOS)
@app.put('/reservas/{reservation_id}')
def update_reserva(reservation_id: str, reserva: ReservationCreate, db: Session = Depends(get_db)):
    """
    Atualiza os detalhes de uma reserva.

    Args:
        reservation_id (str): O ID da reserva que será atualizada.
        reserva (ReservationCreate): Os novos detalhes da reserva.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: Os detalhes atualizados da reserva.
    """
    return crud_reserva.update_reservation(reservation_id, reserva, db)

# CENARIO: DELETAR RESERVA TANTO A SEGELL QUANTO O USUARIO PODERIA FAZER ISSO...
@app.delete('/reservas/{reservation_id}')
def delete_reserva(reservation_id: str, db: Session = Depends(get_db)):
    """
    Deleta uma reserva.

    Args:
        reservation_id (str): O ID da reserva que será deletada.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Uma mensagem indicando que a reserva foi deletada com sucesso.
    """
    crud_reserva.delete_reservation(reservation_id, db)
    return {"detail": "Reserva deletada com sucesso"}

# CENARIO: TELA DO USUARIO COM SUAS RESERVAS
@app.get('/usuario/reservas')
def get_reservas_usuario(current_user: Type = Depends(crud_user.get_current_user), db: Session = Depends(get_db)):
    """
    Obtém as reservas associadas ao usuário atualmente autenticado.

    Args:
        current_user (Type, optional): O usuário atualmente autenticado. Obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de objetos de reserva associados ao usuário.
    """
    return crud_reserva.get_reservations_by_user_id(current_user.id, db)

# CENARIO: RESERVAS FEITAS NAQUELE ID DE RESERVA
@app.get('/usuario/reservas/{reservation_id}')
def get_reserva_usuario(reservation_id: str, current_user: Type = Depends(crud_user.get_current_user), db: Session = Depends(get_db)):
    """
    Obtém uma reserva específica associada ao usuário atualmente autenticado.

    Args:
        reservation_id (str): O ID da reserva a ser obtida.
        current_user (Type, optional): O usuário atualmente autenticado. Obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: O objeto de reserva associado ao usuário, se encontrado.
    
    Raises:
        HTTPException(404): Se a reserva não for encontrada ou não estiver associada ao usuário atual.
    """
    db_reservation = crud_reserva.get_reservation_by_id(reservation_id, db)
    if db_reservation is None or db_reservation.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation
