from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class TipoUser(Base):
    __tablename__ = 'tipouser'

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(200))
    usuarios = relationship('Usuario', back_populates='tipo')


# FIXME: POR ENQUANTO O UNICO JEITO DE CORRIGIR O ERRO É COLOCANDO O TIPO_USER dentro do proprio models do usuario (ERRO expression 'TipoUser' failed to locate a name ('TipoUser'))
