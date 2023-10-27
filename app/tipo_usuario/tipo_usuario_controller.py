from fastapi import Depends
from sqlalchemy.orm import Session
from database.get_db import get_db
from fastapi import APIRouter
from app.tipo_usuario.tipo_usuario_schemas import TipoUserCreate
import app.tipo_usuario.crud_tipo_usuario as crud_tipo_user

router_tipo_usuario = APIRouter()


@router_tipo_usuario.post('/tipos_usuario')
def create_tipo_usuario(tipo_usuario: TipoUserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo tipo de usuário.

    Args:
        tipo_usuario (TipoUsuarioCreate): Os dados do novo tipo de usuário a ser criado.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        TipoUser: O objeto do tipo de usuário criado.
    """
    return crud_tipo_user.create_tipo_usuario(db=db, tipo_usuario=tipo_usuario)

# num sei se eu crio um update ou delete enfim fica a cargo de cleber dizer...