from sqlalchemy.orm import declarative_base

DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    __abstract__ = True
