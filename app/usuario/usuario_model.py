from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class TipoUser(Base):
    __tablename__ = 'tipouser'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(200))
    usuarios = relationship('Usuario', back_populates='tipo')


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    nome = Column(String(100))
    senha = Column(String(200))
    tipo_id = Column(Integer, ForeignKey('tipouser.id'), nullable=False)

    tipo = relationship('TipoUser', back_populates='usuarios')
    reservations = relationship('Reservation', back_populates='usuario')
