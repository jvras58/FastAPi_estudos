from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TipoUser(Base):
    __tablename__ = 'tipouser'

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(200))
    usuarios = relationship('Usuario', back_populates='tipo')
