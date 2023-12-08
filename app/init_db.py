from sqlalchemy.orm import Session

from app.api.tipo_usuario import tipo_usuario_model
from app.database.get_db import get_db


def create(session: Session, model: tipo_usuario_model.TipoUser, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def init_db():
    session = next(get_db())
    create(session, tipo_usuario_model.TipoUser, id=1, tipo='administrador')
    create(session, tipo_usuario_model.TipoUser, id=2, tipo='cliente')
