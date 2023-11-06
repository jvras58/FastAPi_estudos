from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Integer)
    reserva_data = Column(DateTime, default=datetime.utcnow)
    hora_inicio = Column(DateTime)
    hora_fim = Column(DateTime)
    justificacao = Column(String)
    reserva_tipo = Column(String)
    status = Column(String)

    area_id = Column(Integer, ForeignKey('areas.id'))
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

    usuario = relationship('Usuario', back_populates='reservations')
    areas = relationship('Area', back_populates='reservations')
