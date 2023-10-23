from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey,String
from sqlalchemy.orm import relationship
from database.base import Base


class TipoUser(Base):
    __tablename__ = 'tipouser'

    id = Column(UUID, primary_key=True, index=True)
    tipo = Column(String(200))
    usuarios = relationship("Usuario", back_populates="tipo")


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(UUID, primary_key=True, index=True)
    email = Column(String(50),unique=True)
    nome = Column(String(100))
    senha = Column(String(200))
    tipo_id = Column(UUID, ForeignKey('tipouser.id')) 
    
    tipo = relationship("TipoUser", back_populates="usuarios") 
    reservations = relationship("Reservation", back_populates="usuario")
    areas = relationship("Area", back_populates="usuario")