from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.config.auth as auth
from app.api.area.area_model import Area
from app.api.reserva.reserva_model import Reservation
from app.api.tipo_usuario.tipo_usuario_model import TipoUser as tipo
from app.api.usuario.usuario_model import Usuario as User
from app.config.config import get_settings
from app.database.base import Base
from app.database.get_db import get_db as get_session
from app.main import app


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
    """
    Define o pragma de chaves estrangeiras para conexões de banco de dados SQLite.

    Args:
        dbapi_connection: O objeto de conexão com o banco de dados.
        connection_record: O objeto de registro de conexão.
    """
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
    clr_password = 'senhaadm'
    user = User(
        nome='adm test',
        tipo_id=1,
        email='adm.test@example.com',
        senha=auth.get_password_hash(clr_password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clear_password = clr_password
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
    clr_password = 'senhacliente'
    user = User(
        nome='cliente test',
        tipo_id=2,
        email='cliente.test@example.com',
        senha=auth.get_password_hash(clr_password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    user.clear_password = clr_password
    return user


@pytest.fixture
def userCliente2(session):
    """
    Cria uma ingessão de usuarioCliente para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        usuarioCliente: Uma instância de usuarioCliente do sistema.
    """
    clr_password = 'senhacliente2'
    user = User(
        nome='cliente test2',
        tipo_id=2,
        email='cliente.test2@example.com',
        senha=auth.get_password_hash(clr_password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    user.clear_password = clr_password
    return user


@pytest.fixture
def tokenadmin(client, userAdmin):
    """
    cria uma ingessão que efetua login no usuário administrador e retorna um token de acesso.

    Args:
        client: o cliente de teste.
        userAdmin: O usuário administrador.

    Returns:
        O token de acesso como uma string.
    """
    response = client.post(
        '/token',
        data={
            'username': userAdmin.email,
            'password': userAdmin.clear_password,
        },
    )
    return response.json()['access_token']


@pytest.fixture
def tokencliente(client, userCliente):
    """
    cria uma ingessão que efetua login no usuário cliente e retorna um token de acesso.

    Args:
        client: o cliente de teste.
        userCliente: O usuário cliente.

    Returns:
        O token de acesso como uma string.
    """
    response = client.post(
        '/token',
        data={
            'username': userCliente.email,
            'password': userCliente.clear_password,
        },
    )
    return response.json()['access_token']


@pytest.fixture
def tokencliente2(client, userCliente2):
    """
    cria uma ingessão que efetua login no usuário cliente e retorna um token de acesso.

    Args:
        client: o cliente de teste.
        userCliente: O usuário cliente.

    Returns:
        O token de acesso como uma string.
    """
    response = client.post(
        '/token',
        data={
            'username': userCliente2.email,
            'password': userCliente2.clear_password,
        },
    )
    return response.json()['access_token']


@pytest.fixture
def AreaUserAdmin(session):
    """
    Cria uma ingessão de Area para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        userTipoAdmin: Uma instância de Area do sistema.
    """
    area_user = Area(
        nome='Quadra de volei',
        descricao='Uma quadra de volei espaçosa',
        iluminacao='LED',
        tipo_piso='Liso',
        covered='Sim',
        foto_url='https://example.com/quadra_volei.jpg',
    )
    session.add(area_user)
    session.commit()
    session.refresh(area_user)
    return area_user


@pytest.fixture
def ReservaUserAdmin(session):
    """
    Cria uma ingessão de Reservas para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        userTipoAdmin: Uma instância de Reserva do sistema.
    """
    reserva_user = Reservation(
        valor=10,
        reserva_data=datetime.strptime(
            '2023-10-23T12:00:00', '%Y-%m-%dT%H:%M:%S'
        ),
        hora_inicio=datetime.strptime(
            '2023-10-23T14:00:00', '%Y-%m-%dT%H:%M:%S'
        ),
        hora_fim=datetime.strptime('2023-10-23T16:00:00', '%Y-%m-%dT%H:%M:%S'),
        justificacao='Jogo de Equipe',
        reserva_tipo='Jogo',
        status='Em análise',
        area_id=1,
        usuario_id=1,
    )
    session.add(reserva_user)
    session.commit()
    session.refresh(reserva_user)
    return reserva_user


@pytest.fixture
def ReservaUserCliente(session):
    """
    Cria uma ingessão de Reservas para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        userTipoAdmin: Uma instância de Reserva do sistema.
    """
    reserva_user = Reservation(
        valor=10,
        reserva_data=datetime.strptime(
            '2023-10-23T16:00:00', '%Y-%m-%dT%H:%M:%S'
        ),
        hora_inicio=datetime.strptime(
            '2023-10-23T17:00:00', '%Y-%m-%dT%H:%M:%S'
        ),
        hora_fim=datetime.strptime('2023-10-23T19:00:00', '%Y-%m-%dT%H:%M:%S'),
        justificacao='Jogo de Equipe Cliente',
        reserva_tipo='Jogo cliente',
        status='Em análise',
        area_id=1,
        usuario_id=1,
    )
    session.add(reserva_user)
    session.commit()
    session.refresh(reserva_user)
    return reserva_user


@pytest.fixture
def invalid_token():
    """
    Retorna um token JWT inválido para os testes.

    Returns:
        str: Um token JWT inválido.
    """
    return 'invalid_token'


@pytest.fixture
def valid_token_email(userAdmin):
    """
    Retorna um token JWT válido que não contém um campo 'sub'.

    Args:
        userAdmin: Fixture que cria um usuário administrador.

    Returns:
        str: Um token JWT válido sem um campo 'sub' Fazendo assim o token gerado não está associado a nenhum usuario especifico.
    """
    data = {
        'exp': datetime.utcnow()
        + timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(
        data, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM
    )
    return token
