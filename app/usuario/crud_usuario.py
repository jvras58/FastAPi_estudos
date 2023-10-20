from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.area.area_model import Area
from database.get_db import SessionLocal, get_db
from app.reserva.reserva_model import Reservation
from app.usuario.usuario_model import Usuario
from app.usuario.usuario_schemas import UsuarioCreate
import app.security.auth as auth
from typing import Annotated
from jose import JWTError, jwt

SECRET_KEY = "2b9297ddf50a5336ba333962928ce57a1db91464c45c1831d26a4e4b23f5889d"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_user_by_email(email_user: str, db: SessionLocal = Depends(get_db)):
    """
    Obtém um usuário pelo endereço de e-mail.

    Args:
        email_user (str): O endereço de e-mail do usuário a ser obtido.
        db (SessionLocal, optional): Uma sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        Usuario: O usuário correspondente ao endereço de e-mail, ou None se não for encontrado.
    """
    return db.query(Usuario).filter(Usuario.email == email_user).first()

# TODO: MODIFICAÇÕES COM BASE NO PROJETO BASE 
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    """
    Obtém um usuário pelo seu ID.

    Args:
        user_id (str): ID do usuário.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        Usuario: O usuário correspondente ao ID especificado.

    Raises:
        HTTPException: Exceção HTTP com código 404 se o usuário não for encontrado.
    """
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def create_user(db: Session, user: UsuarioCreate):
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
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionLocal = Depends(get_db)):
    """
    Obtém o usuário atual a partir do token de autenticação.

    Args:
        token (str): Token de autenticação.
        db (SessionLocal, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Returns:
        Usuario: O usuário autenticado.
        
    Raises:
        HTTPException: Exceção HTTP com código 401 se as credenciais não puderem ser validadas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db = db, email_user = email)

    if user is None:
        raise credentials_exception
    return user

# TODO: MODIFICAÇÕES COM BASE NO PROJETO BASE 
def get_account_by_id(db: Session, user_id: str):
    """
    Obtém uma conta pelo seu ID.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (str): ID da conta.

    Returns:
        Usuario: O usuário correspondente ao ID especificado.
    """
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_user_by_id(db: Session, id: str):
    """
    Obtém um usuário pelo seu ID.

    Args:
        db (Session): Sessão do banco de dados.
        id (str): ID do usuário.

    Returns:
        Usuario: O usuário correspondente ao ID especificado.

    Raises:
        HTTPException: Exceção HTTP com código 404 se o usuário não for encontrado ou não for do tipo "0".
    """
    user = db.query(Usuario).filter(Usuario.id == id).first()
    if not user or user.tipo != 0:
        raise HTTPException(status_code=404, detail="User not found or invalid type")
    return user

# TODO: MODIFICAÇÕES COM BASE NO PROJETO BASE 
def get_user_reservations(db: Session, user_id: str):
    """
    Obtém o número de reservas associadas a uma conta pelo seu ID.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (str): ID do usuário.

    Returns:
        int: O número de reservas associadas à conta.
    """
    return db.query(Reservation).filter(Reservation.usuario_id == user_id).count()

# TODO: MODIFICAÇÕES COM BASE NO PROJETO BASE 
def get_account_areas(db: Session, user_id: str):
    """
    Obtém o número de áreas associadas a uma conta pelo seu ID.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (str): ID do usuário.

    Returns:
        int: O número de áreas associadas à conta.
    """
    return db.query(Area).filter(Area.usuario_id == user_id).count()
