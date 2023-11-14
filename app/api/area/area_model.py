from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.api.reserva.reserva_model import Reservation


class Area(Base):
    __tablename__ = 'areas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, unique=True, index=False)
    descricao: Mapped[str] = mapped_column(String)
    iluminacao: Mapped[str] = mapped_column(String)
    tipo_piso: Mapped[str] = mapped_column(String)
    covered: Mapped[str] = mapped_column(String)
    foto_url: Mapped[str] = mapped_column(String)

    reservations: Mapped['Reservation'] = relationship(back_populates='areas')
