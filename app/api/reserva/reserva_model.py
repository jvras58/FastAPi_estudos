from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.api.area.area_model import Area
    from app.api.usuario.usuario_model import Usuario


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

    usuario: Mapped['Usuario'] = relationship(
        'Usuario', back_populates='reservations'
    )
    areas: Mapped['Area'] = relationship(back_populates='reservations')
