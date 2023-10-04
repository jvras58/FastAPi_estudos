from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from database.get_db import SessionLocal, get_db
from database.models import Usuario
from database.schemas import UsuarioCreate
import auth
from typing import Annotated
from jose import JWTError, jwt

SECRET_KEY = "2b9297ddf50a5336ba333962928ce57a1db91464c45c1831d26a4e4b23f5889d"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_user_by_email(email_user: str, db: SessionLocal = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.email == email_user).first()

def create_user(db: Session, user: UsuarioCreate):
    db_user = Usuario(**user.model_dump())
    db_user.senha = auth.get_password_hash(db_user.senha)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionLocal = Depends(get_db)):
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