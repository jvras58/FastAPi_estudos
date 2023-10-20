from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Area(Base):
    __tablename__ = "areas"

    id = Column(UUID, primary_key=True, index=True)
    nome = Column(String, unique=True, index=False)
    #disponivel = Column(Boolean)
    descricao = Column(String)
    iluminacao = Column(String)
    tipo_piso = Column(String)
    covered = Column(String)
    foto_url = Column(String)
    
    usuario_id = Column(UUID, ForeignKey("usuario.id"), nullable=True)
    usuario = relationship("Usuario", back_populates="areas")
    reservations = relationship("Reservation", back_populates="areas")