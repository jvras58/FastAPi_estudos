from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.api.reserva.reserva_model import Reservation
    from app.api.tipo_usuario.tipo_usuario_model import TipoUser


class Usuario(Base):
    __tablename__ = 'usuario'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    nome: Mapped[str] = mapped_column(String(100))
    senha: Mapped[str] = mapped_column(String(200))
    tipo_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tipouser.id'),
        nullable=False,
    )
    tipo: Mapped['TipoUser'] = relationship(back_populates='usuarios')
    reservations: Mapped['Reservation'] = relationship(
        back_populates='usuario'
    )
