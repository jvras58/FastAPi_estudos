import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.usuario.usuario_model import TipoUser as tipo
from app.usuario.usuario_model import Usuario as User
from database.base import Base
from database.get_db import get_db as get_session


@pytest.fixture
def client(session):
    """
    Contexto de webclient para teste de APIRest

    Returns:
        TestClient: Uma instancia de TestClient do FastAPI.
    """

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()

    return TestClient(app)


@pytest.fixture
def session():
    """
    Contexto de Session para teste de estrutura de banco de dados.

    Yields:
        Session: Uma instancia de Session do SQLAlchemy
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        # echo=True,
    )

    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


@pytest.fixture
def userTipoAdmin(session):
    """
    Cria uma ingessão de userTipoAdmin para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        userTipoAdmin: Uma instância de userTipoAdmin do sistema.
    """
    tipo_user = tipo(
        id=1,
        tipo='administrador',
    )
    session.add(tipo_user)
    session.commit()
    session.refresh(tipo_user)
    return tipo_user


@pytest.fixture
def userTipoClient(session):
    """
    Cria uma ingessão de userTipoAdmin para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        userTipoAdmin: Uma instância de userTipoAdmin do sistema.
    """
    tipo_user = tipo(
        id=2,
        tipo='cliente',
    )
    session.add(tipo_user)
    session.commit()
    session.refresh(tipo_user)
    return tipo_user


@pytest.fixture
def userAdmin(session):
    """
    Cria uma ingessão de usuarioadm para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        usuarioadm: Uma instância de usuarioadm do sistema.
    """
    user = User(
        nome='adm test',
        tipo_id=1,
        email='adm.test@example.com',
        senha='senhaadm',
    )
    session.add(user)
    session.commit()
    # comentar o refresh permite que o objeto de usuário seja retornado diretamente seria para poder usar em testes que precisa do id no test_get_user_admin mais ainda sim ERROR test/test_usuario.py::test_get_user_admin - sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) FOREIGN KEY constraint failed
    session.refresh(user)
    return user


@pytest.fixture
def userCliente(session):
    """
    Cria uma ingessão de usuarioCliente para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        usuarioCliente: Uma instância de usuarioCliente do sistema.
    """
    user = User(
        nome='cliente test',
        tipo_id=2,
        email='cliente.test@example.com',
        senha='senhacliente',
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
