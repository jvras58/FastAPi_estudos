from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.api.usuario.usuario_model import Usuario

from app.database.base import Base


class TipoUser(Base):
    __tablename__ = 'tipouser'

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(200))
    usuarios: Mapped['Usuario'] = relationship(back_populates='tipo')
