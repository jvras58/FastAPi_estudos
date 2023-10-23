from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey,String
from sqlalchemy.orm import relationship
from database.base import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(UUID, primary_key=True, index=True)
    email = Column(String(50),unique=True)
    nome = Column(String(100))
    senha = Column(String(200))
    # FIXME: teste para verificar o que esta acontecendo entre os relacionamentos... (onde eu comento o tipo_id é o relacionamento tipo_usuario)
    # tipo= Column(String(200))
    tipo_id = Column(UUID, ForeignKey('tipouser.id')) 
    
    tipo = relationship("TipoUser", back_populates="usuarios") 
    reservations = relationship("Reservation", back_populates="usuario")
    areas = relationship("Area", back_populates="usuario")