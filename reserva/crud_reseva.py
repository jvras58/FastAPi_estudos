from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from reserva.reserva_model import Reservation
from reserva.reserva_schema import ReservationCreate

def get_reservation_by_id(reservation_id: str, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def get_reservations_by_user_id(user_id: str, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.usuario_id == user_id).all()

def get_available_reservations(db: Session = Depends(get_db)):
    #FIXME: IMPLEMENTAÇÃO DE TABELA DE STATUS DESCRIÇÃO ONDE CONTEM O STATUS DA DISPONIBILIDADE DA RESERVA
    #return db.query(Reservation).filter(Reservation.status == '1').all()
    return db.query(Reservation).filter(Reservation.disponivel == True).all()

def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
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
    db.delete(db_reservation)
    db.commit()