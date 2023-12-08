from unittest.mock import MagicMock, patch

import bcrypt
import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from jose import jwt

import app.config.auth as auth
from app.api.auth.crud_auth import get_user_permissions

# executa os teste: pytest test/test_auth.py


def test_token_inexistent_user(client):
    """
    Testa se o token não é gerado para um usuário inexistente.
    """
    response = client.post(
        '/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )
    assert response.status_code == 401
    assert 'detail' in response.json()


def test_token_expired_after_time(client, userTipoAdmin, userAdmin):
    """
    Testa se o token expira após um determinado tempo.

    Para isso, o teste utiliza a biblioteca freeze_time para "congelar" o tempo em um momento específico e, em seguida,
    realiza uma requisição para obter um token de acesso. Depois, "congela" o tempo novamente e tenta obter as informações
    do usuário atual utilizando o token obtido anteriormente. Como o token já expirou, a requisição deve retornar um erro 401.
    """
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/token',
            data={
                'username': userAdmin.email,
                'password': userAdmin.clear_password,
            },
        )
        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/areas',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 401
        assert response.json() == {
            'detail': 'Não foi possível validar as credenciais'
        }


def test_refresh_token(client, userTipoAdmin, userAdmin, tokenadmin):
    """
    Testa se o endpoint de atualização de token está funcionando corretamente.
    """
    response = client.post(
        '/refresh_token',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )

    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, userTipoAdmin, userAdmin):
    """
    Testa se o token expirado não é atualizado.

    Verifica se o token expirado não é atualizado ao tentar atualizá-lo com o endpoint /refresh_token.
    """
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/token',
            data={
                'username': userAdmin.email,
                'password': userAdmin.clear_password,
            },
        )
        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 401
        assert response.json() == {
            'detail': 'Não foi possível validar as credenciais'
        }


def test_authenticate_incorrect_password(
    client, session, userTipoAdmin, userAdmin, tokenadmin
):
    """
    Testa a autenticação de um usuário com uma senha incorreta.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        session: Fixture que cria um Objeto de sessão do SQLAlchemy.
        userTipoAdmin: Fixture que cria um usuário com a função 'admin'.
        userAdmin: Fixture que cria um usuário administrador.
        tokenadmin: Fixture que gera um token de acesso para o usuário administrador.

    Returns:
        None
    """
    incorrect_password = 'incorrect_password'
    response = client.post(
        '/token',
        data={'username': userAdmin.email, 'password': incorrect_password},
    )
    assert response.status_code == 401
    assert 'detail' in response.json()


def test_access_invalid_token(client, userTipoAdmin, userAdmin, invalid_token):
    """
    Testa se um token inválido é rejeitado ao tentar obter acesso a rota de criação de areas.

    Args:
    client: objeto test client
    userTipoAdmin: fixture que retorna um usuário com tipo 'admin'
    userAdmin: fixture que retorna um usuário com tipo 'admin'
    invalid_token: fixture que retorna um token inválido
    """
    headers = {'Authorization': f'Bearer {invalid_token}'}
    response = client.post(
        '/areas',
        headers=headers,
    )
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais'
    }


def test_access_token_sem_email(
    client, userTipoAdmin, userAdmin, valid_token_email
):
    """
    Testa se um usuário sem email válido consegue acessar a rota para obter as informações do usuário atual.
    Deve retornar um status code 401 e uma mensagem de erro informando que as credenciais não puderam ser validadas.

    Args:
    client: objeto test client
    userTipoAdmin: fixture que retorna um usuário com tipo 'admin'
    userAdmin: fixture que retorna um usuário com tipo 'admin' e sem email
    valid_token_without_email: fixture que retorna um token válido para o usuário sem email
    """
    headers = {'Authorization': f'Bearer {valid_token_email}'}
    response = client.post(
        '/areas',
        headers=headers,
    )
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais'
    }


def test_not_existent_user(client, userTipoAdmin, userAdmin):
    """
    Testa se um usuário que não existe não pode acessar a rota para obter as informações do usuário atual.

    Verifica se a API retorna um erro 401 quando um usuário não autenticado tenta acessar as informações de um usuário que não existe.

    Para isso, é criado um token de acesso para um usuário que não existe e, em seguida, é feita uma requisição GET para a rota '/usuario/me' com o token do usuário não existente.

    Args:
        client: objeto test client.
        userTipoAdmin: fixture que retorna um usuário do tipo admin.
        userAdmin: fixture que retorna um dicionário com as informações de um usuário do tipo admin.

    """
    not_exist_email = 'not_exist@example.com'
    not_exist_user_token = auth.create_access_token(
        data={'sub': not_exist_email}
    )
    headers = {'Authorization': f'Bearer {not_exist_user_token}'}
    response = client.post(
        '/areas',
        headers=headers,
    )
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais'
    }


@patch('app.api.auth.crud_auth.get_user_permissions')
@patch('app.api.auth.crud_auth.get_user_by_email')
def test_user_without_permissions(
    mock_get_user_by_email, mock_get_user_permissions, client
):
    """
    Testa se a exceção é levantada para um usuário sem permissões.

    Args:
        mock_get_user_by_email: Mock para a função get_user_by_email.
        mock_get_user_permissions: Mock para a função get_user_permissions.
        client: objeto cliente do test_client(FASTAPI).

    Returns:
        None
    """
    password = 'password1234'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    mock_user = MagicMock()
    mock_user.senha = hashed_password.decode('utf-8')
    mock_user.id = 1
    mock_get_user_by_email.return_value = mock_user
    mock_get_user_permissions.return_value = None

    response = client.post(
        '/token',
        data={'username': 'user@example.com', 'password': 'password1234'},
    )

    assert response.status_code == 403
    assert response.json() == {'detail': 'Usuário não tem permissão nenhuma'}


@patch('app.api.auth.crud_auth.Session')
def test_get_user_permissions_with_nonexistent_user(mock_db):
    """
    Testa se a exceção é levantada para um usuário inexistente.

    Args:
        mock_db: Mock para a sessão do banco de dados.

    Returns:
        None
    """
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter().first.return_value = None

    with pytest.raises(HTTPException):
        get_user_permissions(999, mock_db)


def test_incorrect_credential_exception(client, userTipoAdmin, userAdmin):
    """
    Testa a autenticação de um usuário com credenciais incorretas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com a função 'admin'.
        userAdmin: Fixture que cria um usuário administrador.

    Returns:
        None
    """
    incorrect_password = 'incorrect_password'
    response = client.post(
        '/token',
        data={'username': userAdmin.email, 'password': incorrect_password},
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'incorrect username or password'}


def test_jwt():
    data = {'test': 'test', 'permissions': ['administrador']}
    token = auth.create_access_token(data=data)

    decoded = jwt.decode(
        token,
        '2b9297ddf50a5336ba333962928ce57a1db91464c45c1831d26a4e4b23f5889d',
        algorithms=['HS256'],
    )

    assert decoded['test'] == data['test']
    assert decoded['exp']
