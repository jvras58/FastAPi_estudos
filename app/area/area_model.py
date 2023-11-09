from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Area(Base):
    __tablename__ = 'areas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, unique=True, index=False)
    descricao: Mapped[str] = mapped_column(String)
    iluminacao: Mapped[str] = mapped_column(String)
    tipo_piso: Mapped[str] = mapped_column(String)
    covered: Mapped[str] = mapped_column(String)
    foto_url: Mapped[str] = mapped_column(String)

    reservations = relationship('Reservation', back_populates='areas')
