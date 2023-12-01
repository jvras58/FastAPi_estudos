from unittest.mock import patch

from dados_teste import DadosTeste_usuario
from sqlalchemy import select

from app.api.tipo_usuario.tipo_usuario_model import TipoUser as tipo

# executa os teste: pytest test/test_tipos_usuarios.py


def test_estrutura_do_banco_creat_tipo_adm(session):
    """
    Testa a criação de um novo tipo de usuário 'cliente' no banco de dados.
    Verifica se o tipo foi criado corretamente e se é possível recuperá-lo do banco.

    Args:
        session: objeto de sessão do SQLAlchemy.
    """
    tipo_user = tipo(
        id=1,
        tipo='administrador',
    )
    session.add(tipo_user)
    session.commit()
    session.refresh(tipo_user)
    user = session.scalar(select(tipo).where(tipo.tipo == 'administrador'))
    assert user.tipo == 'administrador'


def test_estrutura_do_banco_creat_tipo_cliente(session):
    """
    Testa a criação de um novo tipo de usuário 'cliente' no banco de dados.
    Verifica se o tipo foi criado corretamente e se é possível recuperá-lo do banco.

    Args:
        session: objeto de sessão do SQLAlchemy.
    """
    tipo_user = tipo(
        id=2,
        tipo='cliente',
    )
    session.add(tipo_user)
    session.commit()
    session.refresh(tipo_user)
    user = session.scalar(select(tipo).where(tipo.tipo == 'cliente'))
    assert user.tipo == 'cliente'


def test_post_create_tipo_usuario_adm(client):
    """
    Testa a criação de um tipo de usuário administrador via requisição POST.
    Verifica se a resposta da requisição tem código de status 200 e se o JSON retornado é igual aos dados do tipo de usuário criado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
    """

    tipo_usuario_data_adm = DadosTeste_usuario.tipo_usuario_adm()
    response = client.post('/tipos_usuario', json=tipo_usuario_data_adm)
    assert response.status_code == 200
    assert response.json() == tipo_usuario_data_adm


def test_post_create_tipo_usuario_adm_ja_exist(client, userTipoAdmin):
    """
    Testa a criação de um tipo de usuário administrador via requisição POST.
    Verifica se a resposta da requisição tem código de status 200 e se o JSON retornado é igual aos dados do tipo de usuário criado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
    """

    tipo_usuario_data_adm = DadosTeste_usuario.tipo_usuario_adm()
    response = client.post('/tipos_usuario', json=tipo_usuario_data_adm)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Tipo de usuário já existe'}


def test_post_create_tipo_usuario_cliente(client):
    """
    Testa a criação de um tipo de usuário cliente via requisição POST.

    Verifica se a resposta da requisição tem código de status 200 e se o JSON retornado é igual aos dados do tipo de usuário criado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
    """
    tipo_usuario_data_cliente = DadosTeste_usuario.tipo_usuario_cliente()
    response = client.post('/tipos_usuario', json=tipo_usuario_data_cliente)
    assert response.status_code == 200
    assert response.json() == tipo_usuario_data_cliente


def test_read_tipos_usuario(client, userTipoAdmin, tokenadmin):
    """
    Testa se é possível obter uma lista de tipos de usuário.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação do usuário administrador.
    """
    response = client.get(
        '/tipos_usuario',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json() == {'tipos': [{'id': 1, 'tipo': 'administrador'}]}
    assert len(response.json()) > 0


def test_read_tipo_users_exception(client):
    """
    Testa se a exceção é lançada corretamente quando não há tipos de usuários.
    """
    with patch(
        'app.api.tipo_usuario.crud_tipo_usuario.get_tipo_usuarios'
    ) as mock_get_tipo_usuarios:
        mock_get_tipo_usuarios.return_value = None

        response = client.get('/tipos_usuario')

        assert response.status_code == 404
        assert response.json() == {'detail': 'Tipo de usuário não encontrado'}
    assert response.json() == {'detail': 'Tipo de usuário não encontrado'}


def test_read_tipos_usuario_with_users(client, userTipoAdmin, tokenadmin):
    """
    Testa se o endpoint '/tipos_usuario/' retorna as informações corretas dos tipos de usuário.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com privilégios de administrador.
        tokenadmin: token de autenticação do usuário administrador.
    """
    response = client.get(
        '/tipos_usuario/',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json() == {'tipos': [{'id': 1, 'tipo': 'administrador'}]}


@patch('app.api.tipo_usuario.crud_tipo_usuario.get_tipo_usuarios')
def test_read_tipo_users_exception2(mock_get_tipo_usuarios, client):
    mock_get_tipo_usuarios.return_value = None

    response = client.get('/tipos_usuario')

    assert response.status_code == 404
    assert response.json() == {'detail': 'Tipo de usuário não encontrado'}


def test_update_tipos_usuarios(client, userTipoAdmin, tokenadmin):
    """
    Testa se é possível atualizar um tipo de usuário.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com privilégios de administrador.
        tokenadmin: token de autenticação do usuário administrador.
    """
    response = client.put(
        '/tipos_usuario/1',
        json={'id': 1, 'tipo': 'cliente'},
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'tipo': 'cliente'}


def test_update_tipos_usuarios_not_found(client, userTipoAdmin, tokenadmin):
    """
    Testa se a rota retorna a exceção correta quando o tipo de usuário não é encontrado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com privilégios de administrador.
        tokenadmin: token de autenticação do usuário administrador.
    """
    response = client.put(
        '/tipos_usuario/2',
        json={'id': 2, 'tipo': 'cliente'},
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Tipo de usuário não encontrado'}


def test_delete_tipos_usuarios(
    client, userTipoAdmin, userTipoClient, tokenadmin
):
    """
    Testa se é possível deletar um tipo de usuário.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com privilégios de administrador.
        tokenadmin: token de autenticação do usuário administrador.
    """
    response = client.delete(
        f'/tipos_usuario/{userTipoAdmin.id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json() == {
        'detail': 'Tipo de usuário excluído com sucesso usuarios reatribuidos ao tipo de usuário padrão'
    }


def test_delete_tipos_usuarios_not_found(client, userTipoAdmin, tokenadmin):
    """
    Testa se a rota retorna a exceção correta quando o tipo de usuário não é encontrado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com privilégios de administrador.
        tokenadmin: token de autenticação do usuário administrador.
    """
    response = client.delete(
        '/tipos_usuario/2',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Tipo de usuário não encontrado'}
