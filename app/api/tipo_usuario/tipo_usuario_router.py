from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.api.tipo_usuario.crud_tipo_usuario as crud_tipo_user
from app.api.tipo_usuario.tipo_usuario_schemas import TipoUserCreate
from app.database.get_db import get_db

router_tipo_usuario = APIRouter()

Session = Annotated[Session, Depends(get_db)]


@router_tipo_usuario.post('/tipos_usuario')
def create_tipo_usuario(tipo_usuario: TipoUserCreate, db: Session):
    """
    Cria um novo tipo de usuário.

    Args:
        tipo_usuario (TipoUsuarioCreate): Os dados do novo tipo de usuário a ser criado.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        TipoUser: O objeto do tipo de usuário criado.
    """
    return crud_tipo_user.create_tipo_usuario(db=db, tipo_usuario=tipo_usuario)
