from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String
from sqlalchemy.orm import relationship
from database.base import Base

class TipoUser(Base):
    __tablename__ = 'tipouser'

    id = Column(UUID, primary_key=True, index=True)
    tipo = Column(String(200))
    usuarios = relationship("Usuario", back_populates="tipo")