#from sqlalchemy.dialects.postgresql import UUID
#from sqlalchemy import Column,String
#from sqlalchemy.orm import relationship
#from database.base import Base

# muitos-para-um (um usuário pode ter um tipo associado, mas um tipo pode estar associado a vários usuários).
#class TipoUser(Base):
#    __tablename__ = 'tipouser'

#    id = Column(UUID, primary_key=True, index=True)
#    tipo = Column(String(200))
#    usuarios = relationship("Usuario", back_populates="tipo")


#FIXME: POR ENQUANTO O UNICO JEITO DE CORRIGIR O ERRO É COLOCANDO O TIPO_USER dentro do proprio models do usuario (ERRO expression 'TipoUser' failed to locate a name ('TipoUser'))
