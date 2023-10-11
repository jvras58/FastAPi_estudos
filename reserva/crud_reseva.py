from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from reserva.reserva_model import Reservation
from reserva.reserva_schema import ReservationCreate
from area.area_model import Area

def get_reservation_by_id(reservation_id: str, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def get_reservations_by_user_id(user_id: str, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.usuario_id == user_id).all()

def get_available_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.disponivel == True).all()

# TESTME: TESTAR A ROTA DE /areas/disponiveis para ver se esta funcionando corretamente
def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    
    # Agora, após a reserva ser criada, atualize a disponibilidade da área associada
    area_id = reservation.area_id
    db_area = db.query(Area).filter(Area.id == area_id).first()
    
    if db_area:
        db_area.disponivel = False  # Marcar a área como indisponível
        db.commit()
    
    return db_reservation


def update_reservation(reservation_id: str, reservation: ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = get_reservation_by_id(reservation_id, db)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    for key, value in reservation.model_dump().items():
        setattr(db_reservation, key, value)
    db.commit()
    return db_reservation

def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = get_reservation_by_id(reservation_id, db)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # Antes de excluir a reserva, obtenha o ID da área associada
    area_id = db_reservation.area_id
    
    # Exclua a reserva
    db.delete(db_reservation)
    db.commit()
    
    # Agora, após a reserva ser excluída, atualize a disponibilidade da área associada
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if db_area:
        db_area.disponivel = True  # Marcar a área como disponível
        db.commit()
