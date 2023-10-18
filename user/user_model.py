from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String
from sqlalchemy.orm import relationship
from database.base import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(UUID, primary_key=True, index=True)
    email = Column(String(50),unique=True)
    nome = Column(String(100))
    senha = Column(String(200))

    reservations = relationship("Reservation", back_populates="usuario")

