from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from reserva.reserva_model import Reservation
from reserva.reserva_schema import ReservationCreate
from area.area_model import Area
from fastapi.encoders import jsonable_encoder


def get_reservation_by_id(reservation_id: str, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def get_reservations_by_user_id(user_id: str, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.usuario_id == user_id).all()

def get_available_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.disponivel == True).all()


def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    # Antes de criar a reserva obtenha o id da área associada
    area_id = reservation.area_id
    db_area = db.query(Area).filter(Area.id == area_id).first()
    
    # apos a reserva ser criada atualiza a disponibilidade da area associada
    if db_area:
        db_area.disponivel = False 
    # FIXME: se comentar o db.commit corrige o problema? mas qual problema isso me causaria kkk isso não serve pra enviar as coisas pro banco?? so deus sabe kk (vou deixar com o print por enquanto)
        db.commit()
    # FIXME: BUG NO JSON DO CREATE_RESERVATION MAS QUE  BUG É ESSE?? ELE PRECISA DOS PRINTS PRA ME RETORNAR O db_reservation no body do swagger ?? QUE SEM SENTIDO KKK (consegui reduzir a quantidade de print para um print só kk)

        print(db_reservation.id)

    
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
    
    # Antes de excluir a reserva obtenha o id da área associada
    area_id = db_reservation.area_id
    db.delete(db_reservation)
    db.commit()
    
    # após a reserva ser excluída, atualiza a disponibilidade da área associada
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if db_area:
        db_area.disponivel = True  # Marca disponível
        db.commit()
