from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.get_db import get_db
from fastapi import APIRouter
from typing import Type

#user
import app.usuario.crud_usuario as crud_usuario

# reservas
from app.reserva.reserva_schema import ReservationCreate
import app.reserva.crud_reserva as crud_reserva

router = APIRouter()

@router.post('/reservas')
def create_reserva(reserva: ReservationCreate, db: Session = Depends(get_db)):
    """
    Criar uma nova reserva.

    Args:
        reserva (ReservationCreate): Os detalhes da reserva a ser criada.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: A reserva criada.
    """
    #return crud_reserva.create_reservation(db=db, reservation=reserva)
    response = crud_reserva.create_reservation(db=db, reservation=reserva)
    if response is None:
        raise HTTPException(status_code=400, detail="Horário indiponível para essa Área")
    return response


@router.get('/reservas')
def get_all_reservas(db: Session = Depends(get_db)):
    """
    Visualiza todas as reservas.

    Args:
        
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservas: Todas as reservas.
    """  
    return crud_reserva.get_all(db)



@router.get('/reservas/disponiveis')
def get_reservas_disponiveis(db: Session = Depends(get_db)):
    """
    Obter a lista de reservas disponíveis.

    Args:
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de reservas disponíveis.
    """
    return crud_reserva.get_available_reservations(db)


@router.get('/reservas/{reservation_id}')
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

@router.put('/reservas/{reservation_id}')
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

@router.delete('/reservas/{reservation_id}')
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

@router.get('/usuario/reservas')
def get_reservas_usuario(current_user: Type = Depends(crud_usuario.get_current_user), db: Session = Depends(get_db)):
    """
    Obtém as reservas associadas ao usuário atualmente autenticado.

    Args:
        current_user (Type, optional): O usuário atualmente autenticado. Obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de objetos de reserva associados ao usuário.
    """
    return crud_reserva.get_reservations_by_user_id(current_user.id, db)

@router.get('/usuario/reservas/{reservation_id}')
def get_reserva_usuario(reservation_id: str, current_user: Type = Depends(crud_usuario.get_current_user), db: Session = Depends(get_db)):
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