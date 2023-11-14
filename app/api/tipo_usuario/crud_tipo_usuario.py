from sqlalchemy.orm import Session

from app.api.tipo_usuario.tipo_usuario_model import TipoUser
from app.api.tipo_usuario.tipo_usuario_schemas import TipoUserCreate


def create_tipo_usuario(db: Session, tipo_usuario: TipoUserCreate):
    """
    Cria um novo tipo de usuário.

    Args:
        tipo_usuario (TipoUsuarioCreate): Os dados do novo tipo de usuário a ser criado.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        TipoUser: O objeto do tipo de usuário criado.
    """
    db_tipo_usuario = TipoUser(**tipo_usuario.model_dump())
    db.add(db_tipo_usuario)
    db.commit()
    db.refresh(db_tipo_usuario)
    return db_tipo_usuario
