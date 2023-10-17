from sqlalchemy.orm import Session
from database.get_db import SessionLocal
from user.user_schemas import UsuarioCreate
from user.user_model import Usuario
import security.auth as auth
from typing import Optional

def get_user_by_email(email_user: str, db: Session):
    """
    Obtém um usuário pelo endereço de e-mail.

    Args:
        email_user (str): O endereço de e-mail do usuário a ser obtido.
        db (SessionLocal, optional): Uma sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        Usuario: O usuário correspondente ao endereço de e-mail, ou None se não for encontrado.
    """
    return db.query(Usuario).filter(Usuario.email == email_user).first()

def create_new_user(db: Session, user: UsuarioCreate):
    """
    Cria um novo usuário no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        user (UsuarioCreate): Os dados do usuário a serem criados.

    Returns:
        Usuario: O usuário criado.
    """
    db_user = Usuario(**user.model_dump())
    db_user.senha = auth.get_password_hash(db_user.senha)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: Session):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def update_user_info(user_id: int, new_data: dict, db: Session):
    db.query(Usuario).filter(Usuario.id == user_id).update(new_data)
    db.commit()
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def remove_user(user_id: int, db: Session):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    db.delete(user)
    db.commit()
    return user

def register_user(db: Session, user_data: UsuarioCreate):
    existing_user = get_user_by_email(user_data.email, db)
    if existing_user:
        return None  # Usuário já existe, pode adicionar uma lógica de tratamento aqui se desejar

    return create_new_user(db, user_data)

def update_user_information(db: Session, user_id: int, new_data: dict):
    return update_user_info(user_id, new_data, db)

def delete_user(db: Session, user_id: int):
    return remove_user(user_id, db)
