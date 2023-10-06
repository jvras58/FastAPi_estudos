from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,String
from sqlalchemy.orm import relationship
from database.base import Base

# Usuário:tem uma relação de um para muitos com as tabelas Reserva e Área. Cada usuário pode ter várias reservas e áreas.

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(UUID, primary_key=True, index=True)
    email = Column(String(50), primary_key=True)
    nome = Column(String(100))
    senha = Column(String(200))

    reservations = relationship("Reservation", back_populates="usuario")
    areas = relationship("Area", back_populates="usuario")













# -------------------------------------------------------------------------teste--------------------------------------------------------------------------------------------------------------------------------------------------- #
# # Área: Esta tabela tem uma relação de um para muitos com a tabela Reserva. Cada área pode ter várias reservas. Além disso, tem uma relação de muitos para um com a tabela Usuário. Cada área está associada a um usuário.
# class Area(Base):
#     __tablename__ = "areas"

#     id = Column(UUID, primary_key=True, index=True)
#     nome = Column(String, unique=True, index=False)
#     disponivel = Column(Boolean)
#     descricao = Column(String)
#     iluminacao = Column(String)
#     tipo_piso = Column(String)
#     covered = Column(String)
#     foto_url = Column(String)
#     usuario_id = Column(UUID, ForeignKey("usuario.id"), nullable=True)

#     usuario = relationship("Usuario", back_populates="areas")
#     reservations = relationship("Reservation", back_populates="areas")

# # Reserva: Esta tabela tem uma relação de muitos para um com as tabelas Usuário e Área. Cada reserva está associada a um usuário e uma área.
# class Reservation(Base):
#     __tablename__ = "reservations"

#     id = Column(UUID, primary_key=True, index=True)
#     valor = Column(Integer)
#     reserva_data= Column(DateTime, default=datetime.utcnow)
#     hora_inicio = Column(DateTime)
#     hora_fim = Column(DateTime)
#     justificacao = Column(String)
#     reserva_tipo = Column(String)
#     status = Column(String)
#     area_id = Column(UUID, ForeignKey("areas.id"))
#     usuario_id = Column(UUID, ForeignKey("usuario.id"))

#     usuario = relationship("Usuario", back_populates="reservations")
#     areas = relationship("Area", back_populates="reservations")