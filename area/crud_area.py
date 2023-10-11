from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.get_db import SessionLocal, get_db
from area.area_model import Area
from area.area_schema import AreaCreate

def get_area_by_id(area_id: str, db: Session = Depends(get_db)):
    return db.query(Area).filter(Area.id == area_id).first()


def get_available_areas(db: Session = Depends(get_db)):
    return db.query(Area).filter(Area.disponivel == True).all()


def create_area(db: Session, area: AreaCreate):
    db_area = db.query(Area).filter(Area.nome == area.nome).first()
    if db_area:
        raise HTTPException(status_code=400, detail="Area already exists")
    db_area = Area(**area.model_dump())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


def update_area(area_id: str, area: AreaCreate, db: Session = Depends(get_db)):
    db_area = get_area_by_id(area_id, db)
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    for key, value in area.model_dump().items():
        setattr(db_area, key, value)
    db.commit()
    return db_area

def delete_area(area_id: str, db: Session = Depends(get_db)):
    db_area = get_area_by_id(area_id, db)
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    db.delete(db_area)
    db.commit()