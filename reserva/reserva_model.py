from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy import Column,Integer, String,DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.base import Base

# Reserva: Esta tabela tem uma relação de muitos para um com as tabelas Usuário e Área. Cada reserva está associada a um usuário e uma área.
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(UUID, primary_key=True, index=True)
    valor = Column(Integer)
    reserva_data= Column(DateTime, default=datetime.utcnow)
    hora_inicio = Column(DateTime)
    hora_fim = Column(DateTime)
    justificacao = Column(String)
    reserva_tipo = Column(String)
    #FIXME: IMPLEMENTAÇÃO DE TABELA DE STATUS DESCRIÇÃO ONDE CONTEM O STATUS DA DISPONIBILIDADE DA RESERVA
    status = Column(String)
    # GAMBIARRA POR ENQUANTO PARA TER SO DOIS STATUS KK 
    disponivel = Column(Boolean)
    area_id = Column(UUID, ForeignKey("areas.id"))
    usuario_id = Column(UUID, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="reservations")
    areas = relationship("Area", back_populates="reservations")