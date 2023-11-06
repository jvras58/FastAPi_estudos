from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import app.security.auth as auth

# from app.area.area_model import Area
from app.reserva.reserva_model import Reservation
from app.usuario.usuario_model import Usuario
from app.usuario.usuario_schemas import UsuarioCreate
from database.get_db import SessionLocal, get_db

SECRET_KEY = '2b9297ddf50a5336ba333962928ce57a1db91464c45c1831d26a4e4b23f5889d'
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


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


def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Obtém um usuário pelo seu ID.

    Args:
        user_id (int): ID do usuário.
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


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: SessionLocal = Depends(get_db),
):
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
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db=db, email_user=email)
    if user is None:
        raise credentials_exception
    return user


def get_account_by_id(db: Session, user_id: int):
    """
    Obtém uma conta pelo seu ID.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID da conta.

    Returns:
        Usuario: O usuário correspondente ao ID especificado.
    """
    return db.query(Usuario).filter(Usuario.id == user_id).first()


def get_current_admin_user(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtém o usuário autenticado com privilégios de administrador.

    Args:
        current_user (Usuario): O usuário atual autenticado.
        db (Session): A sessão do banco de dados para consulta.

    Returns:
        Usuario: O usuário autenticado com privilégios de administrador.

    Raises:
        HTTPException(403): Se o usuário não tiver privilégios de administrador.
    """
    if not is_admin(current_user.id, db):
        raise HTTPException(
            status_code=403,
            detail='Permissão negada. Somente administradores podem acessar esta rota.',
        )
    return current_user


def is_admin(user_id: int, db: Session):
    """
    Verifica se o usuário possui privilégios de administrador.

    Args:
        user_id (int): O ID do usuário a ser verificado.
        db (Session): A sessão do banco de dados para consulta.

    Returns:
        bool: True se o usuário é um administrador, False caso contrário.

    Raises:
        HTTPException: Se o usuário não for encontrado no banco de dados.
    """
    user = get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='Usuário com privilegios de adm não encontrado',
        )
    return user.tipo.tipo == 'administrador'


def get_user_reservations(user_id: int, db: Session):
    """
    Obtém o número de reservas associadas a uma conta pelo seu ID.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID do usuário.

    Returns:
        int: O número de reservas associadas à conta.
    """
    return (
        db.query(Reservation).filter(Reservation.usuario_id == user_id).count()
    )


# TODO: PODE SER UMA LISTA COM AS RESERVAS TBM ISSO QUEM VAI ESCOLHER É O FRONTER MAS POR ENQUANTO VOU DEIXAR A QUANTIDADE MSM
def get_user_reservations1(user_id: int, db: Session):
    """
     Obtém as reservas associadas a um usuário pelo seu ID.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID do usuário.

    Returns:
        List[reservas]: Lista de reservas associadas ao usuário.
    """
    user = get_user_by_id(user_id, db)
    if user:
        return user.reservations
    return None


# #TEST: verificar se está funcionando como esperado
def get_user_areas1(user_id: int, db: Session):
    """
    Obtém as áreas associadas a um usuário pelo seu ID.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID do usuário.

    Returns:
        Tuple[List[Area], int]: Lista de áreas associadas ao usuário e a quantidade de áreas.
    """
    user = get_user_by_id(user_id, db)
    if user:
        Reservation = user.reservations
        return Reservation, len(Reservation)
    return None, 0


def update_user_password(db: Session, user: Usuario, new_password: str):
    """
    Atualiza a senha de um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user (Usuario): O usuário cuja senha será atualizada.
        new_password (str): A nova senha do usuário.
    """
    user.senha = auth.get_password_hash(new_password)
    db.commit()


def delete_user(db: Session, user: Usuario):
    """
    Deleta um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user (Usuario): O usuário a ser deletado.
    """
    db.delete(user)
    db.commit()


def delete_user_by_id(user_id: int, db: Session):
    """
    Deleta um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): O ID do usuário a ser deletado.
    """
    user = get_user_by_id(user_id, db)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def update_user(user_id: int, usuario: UsuarioCreate, db: Session):
    """
    Atualiza os detalhes de um usuário.

    Args:
        db (Session): Sessão do banco de dados.
        user_id (int): ID do usuário a ser atualizado.
        user_update (UsuarioCreate): Os novos detalhes do usuário.

    Returns:
        Usuario: O usuário atualizado.
    """
    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    # itens é um método de dicionário que retorna uma lista de tuplas, onde cada tupla contém um par chave-valor(no nosso caso dado-valor[ex: {'nome': 'Novo Nome'}]) do dicionário.
    for dado, valor in usuario.model_dump().items():
        # O setattr é uma função embutida em Python que define o valor de um atributo de um objeto. Neste caso, estamos configurando o atributo key (que é o nome do campo) do objeto user para ter o valor value.
        setattr(user, dado, valor)
    db.commit()
    db.refresh(user)
    return user
