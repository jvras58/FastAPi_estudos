from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Reservation(Base):
    __tablename__ = 'reservations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    valor: Mapped[int] = mapped_column(Integer)
    reserva_data: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    hora_inicio: Mapped[DateTime] = mapped_column(DateTime)
    hora_fim: Mapped[DateTime] = mapped_column(DateTime)
    justificacao: Mapped[str] = mapped_column(String)
    reserva_tipo: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    area_id: Mapped[int] = mapped_column(Integer, ForeignKey('areas.id'))
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.id'))

    usuario = relationship('Usuario', back_populates='reservations')
    areas = relationship('Area', back_populates='reservations')
