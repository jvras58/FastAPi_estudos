from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    nome: Mapped[str] = mapped_column(String(100))
    senha: Mapped[str] = mapped_column(String(200))
    tipo_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('tipouser.id'), nullable=False
    )
    tipo = relationship('TipoUser', back_populates='usuarios')
    reservations = relationship('Reservation', back_populates='usuario')


class TipoUser(Base):
    __tablename__ = 'tipouser'

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(200))
    usuarios = relationship('Usuario', back_populates='tipo')
