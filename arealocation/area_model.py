from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

# Área: Esta tabela tem uma relação de um para muitos com a tabela Reserva. Cada área pode ter várias reservas. Além disso, tem uma relação de muitos para um com a tabela Usuário. Cada área está associada a um usuário.

class Area(Base):
    __tablename__ = "areas"

    id = Column(UUID, primary_key=True, index=True)
    nome = Column(String, unique=True, index=False)
    disponivel = Column(Boolean)
    descricao = Column(String)
    iluminacao = Column(String)
    tipo_piso = Column(String)
    covered = Column(String)
    foto_url = Column(String)
    
    # RELACIONAMENTO de muitos para um com a classe Usuario removida
    # para mim ainda faz sentido esse relacionemento existir pq tipo usuario não é so usuario cliente ne.... se um usuário é também o proprietário de uma ou mais quadras e outros usuários podem alugar essas quadras
    #usuario_id = Column(UUID, ForeignKey("usuario.id"), nullable=True)
    #usuario = relationship("Usuario", back_populates="areas")
    reservations = relationship("Reservation", back_populates="areas")