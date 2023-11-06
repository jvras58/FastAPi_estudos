from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class TipoUser(Base):
    __tablename__ = 'tipouser'

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(200))
    usuarios = relationship('Usuario', back_populates='tipo')


# FIXME: POR ENQUANTO O UNICO JEITO DE CORRIGIR O ERRO É COLOCANDO O TIPO_USER dentro do proprio models do usuario (ERRO expression 'TipoUser' failed to locate a name ('TipoUser'))
