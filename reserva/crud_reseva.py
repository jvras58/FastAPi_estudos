from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from reserva.reserva_model import Reservation
from reserva.reserva_schema import ReservationCreate
from area.area_model import Area



def get_reservation_by_id(reservation_id: str, db: Session = Depends(get_db)):
    """
    Obtém uma reserva pelo seu ID.

    Args:
        reservation_id (str): O ID da reserva a ser obtida.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: A reserva encontrada com o ID correspondente, ou None se não encontrada.
    """
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def get_reservations_by_user_id(user_id: str, db: Session = Depends(get_db)):
    """
    Obtém todas as reservas associadas a um usuário pelo seu ID.

    Args:
        user_id (str): O ID do usuário para o qual as reservas estão associadas.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de reservas associadas ao usuário, ou uma lista vazia se não houver nenhuma.
    """
    return db.query(Reservation).filter(Reservation.usuario_id == user_id).all()

def get_available_reservations(db: Session = Depends(get_db)):
    """
    Obtém todas as reservas disponíveis no banco de dados.

    Args:
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de reservas disponíveis, ou uma lista vazia se não houver nenhuma.
    """
    return db.query(Reservation).filter(Reservation.disponivel == True).all()


# TODO: CORREÇÃO DE CONDIÇÃO PARA CRIAÇÃO DE RESERVA PARA DEFINIR SE É DISPONIVEL OU NÃO POR HORARIO
def create_reservation(db: Session, reservation: ReservationCreate):
    """
    Cria uma nova reserva no banco de dados.

    Args:
        db (Session): Uma sessão do banco de dados.
        reservation (ReservationCreate): Os dados da reserva a ser criada.

    Returns:
        Reservation: A reserva criada.
    """
    # Antes de criar a reserva obtenha o id da área associada
    area_id = reservation.area_id

    # Verificar se há conflito de horários
    inicio = reservation.hora_inicio
    fim = reservation.hora_fim

    reservas_conflito = db.query(Reservation).filter(
        Reservation.area_id == area_id,
        Reservation.reserva_data == reservation.reserva_data,
        Reservation.hora_inicio < fim,
        Reservation.hora_fim > inicio
    ).all()

    if reservas_conflito:
        return None

    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)


    # eu realmente não sei se é necessario ou não manter essa atualização nas tabelas pára verificar se a area esta disponivel de acordo com jova não é,,,,
    
    # # Após a reserva ser criada, atualiza a disponibilidade da área associada
    # db_area = db.query(Area).filter(Area.id == area_id).first()
    # if db_area:
    #     db_area.disponivel = False 
    #     db.commit()

    return db_reservation

    

def update_reservation(reservation_id: str, reservation: ReservationCreate, db: Session = Depends(get_db)):
    """
    Atualiza os detalhes de uma reserva existente.

    Args:
        reservation_id (str): O ID da reserva a ser atualizada.
        reservation (ReservationCreate): Os novos detalhes da reserva.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Raises:
        HTTPException: Retorna um erro 404 se a reserva não for encontrada.

    Returns:
        Reservation: A reserva atualizada.
    """
    db_reservation = get_reservation_by_id(reservation_id, db)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    for key, value in reservation.model_dump().items():
        setattr(db_reservation, key, value)
    db.commit()
    return db_reservation

def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    """
    Exclui uma reserva existente.

    Args:
        reservation_id (str): O ID da reserva a ser excluída.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Raises:
        HTTPException: Retorna um erro 404 se a reserva não for encontrada.

    Returns:
        dict: Um dicionário com uma mensagem indicando que a reserva foi excluída com sucesso.
    """
    db_reservation = get_reservation_by_id(reservation_id, db)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # Antes de excluir a reserva obtenha o id da área associada
    area_id = db_reservation.area_id
    db.delete(db_reservation)
    db.commit()
    
    # após a reserva ser excluída, atualiza a disponibilidade da área associada
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if db_area:
        db_area.disponivel = True  # Marca disponível
        db.commit()