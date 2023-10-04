from sqlalchemy import Column, Float, ForeignKeyConstraint, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base



DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    __abstract__ = True

class Usuario(Base):
    __tablename__ = 'usuario'

    email = Column(String(50), primary_key=True)
    nome = Column(String(100))
    senha = Column(String(200))

