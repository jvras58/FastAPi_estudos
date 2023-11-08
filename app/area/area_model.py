from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class Area(Base):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=False)
    descricao = Column(String)
    iluminacao = Column(String)
    tipo_piso = Column(String)
    covered = Column(String)
    foto_url = Column(String)

    reservations = relationship('Reservation', back_populates='areas')
