from unittest.mock import patch

import pytest
from dados_teste import DadosTeste_usuario
from sqlalchemy import select

import app.api.tipo_usuario.crud_tipo_usuario as crud_tipo_user
from app.api.tipo_usuario.tipo_usuario_model import TipoUser as tipo
from app.utils.Exceptions.exceptions import ObjectNotFoundException

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


# def test_estrutura_do_banco_creat_tipo_adm_exception_objet_exist(session):
#     """
#     Testa a criação de um novo tipo de usuário 'cliente' no banco de dados.
#     Verifica se o tipo foi criado corretamente e se é possível recuperá-lo do banco.

#     Args:
#         session: objeto de sessão do SQLAlchemy.
#     """

#     tipo_user = TipoUserCreate(
#         id=1,
#         tipo='administrador',
#     )

#     # Simula a existência do tipo de usuário no banco de dados
#     existing_tipo_user = tipo(id=1, tipo='administrador')
#     session.add(existing_tipo_user)
#     session.commit()

#     try:
#         with patch('app.api.tipo_usuario.crud_tipo_usuario', session):
#             create_tipo_usuario(session, tipo_user)
#     except IntegrityError:
#         session.rollback()
#         raise HTTPException(
#             status_code=400, detail='ID já existe no banco de dados.'
#         )


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
    assert response.status_code == 409
    assert 'detail' in response.json()


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
    assert 'detail' in response.json()


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
    assert 'detail' in response.json()


def test_delete_tipos_usuarios_exception(client, userTipoAdmin, tokenadmin):
    """
    Testa se a rota DELETE retorna a exceção correta quando o tipo de usuário não é encontrado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com privilégios de administrador.
        tokenadmin: token de autenticação do usuário administrador.
    """
    with patch(
        'app.api.tipo_usuario.crud_tipo_usuario.get_tipo_usuario'
    ) as mock_get:
        mock_get.side_effect = ObjectNotFoundException(
            'Tipo de usuário não encontrado', ''
        )

        response = client.delete(
            '/tipos_usuario/999',
            headers={'Authorization': f'Bearer {tokenadmin}'},
        )

        assert response.status_code == 404
        assert 'detail' in response.json()


def test_delete_tipos_usuarios_exception_get_tipo_usuario(
    client, userTipoAdmin, tokenadmin
):
    """
    Testa se a rota DELETE retorna a exceção correta quando o tipo de usuário não é encontrado na função get_tipo_usuario.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com privilégios de administrador.
        tokenadmin: token de autenticação do usuário administrador.
    """
    with patch(
        'app.api.tipo_usuario.crud_tipo_usuario.get_tipo_usuario'
    ) as mock_get:
        mock_get.side_effect = ObjectNotFoundException(
            'Tipo de usuário não encontrado', ''
        )

        response = client.delete(
            '/tipos_usuario/999',
            headers={'Authorization': f'Bearer {tokenadmin}'},
        )

        assert response.status_code == 404
        assert 'detail' in response.json()


def test_delete_tipos_usuarios_exception_reassign_users_and_delete_tipo_usuario(
    client, userTipoAdmin, tokenadmin
):
    """
    Testa se a rota DELETE retorna a exceção correta quando o tipo de usuário não é encontrado na função reassign_users_and_delete_tipo_usuario.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com privilégios de administrador.
        tokenadmin: token de autenticação do usuário administrador.
    """
    with patch(
        'app.api.tipo_usuario.crud_tipo_usuario.reassign_users_and_delete_tipo_usuario'
    ) as mock_reassign:
        mock_reassign.side_effect = ObjectNotFoundException(
            'Tipo de usuário não encontrado', ''
        )

        response = client.delete(
            '/tipos_usuario/999',
            headers={'Authorization': f'Bearer {tokenadmin}'},
        )

        assert response.status_code == 404
        assert 'detail' in response.json()


def test_delete_tipos_usuarios_exception_get_tipo_usuario1(
    client, userTipoAdmin, tokenadmin
):
    with patch(
        'app.api.tipo_usuario.crud_tipo_usuario.get_tipo_usuario'
    ) as mock_get:
        mock_get.side_effect = ObjectNotFoundException(
            'Tipo de usuário não encontrado', ''
        )

        response = client.delete(
            '/tipos_usuario/999',
            headers={'Authorization': f'Bearer {tokenadmin}'},
        )

        assert response.status_code == 404
        assert 'detail' in response.json()


def test_delete_tipos_usuarios_exception_get_tipo_usuarios(
    client, userTipoAdmin, tokenadmin
):
    with patch(
        'app.api.tipo_usuario.crud_tipo_usuario.get_tipo_usuarios'
    ) as mock_get_all:
        mock_get_all.side_effect = ObjectNotFoundException(
            'Tipo de usuário não encontrado', ''
        )

        response = client.delete(
            '/tipos_usuario/999',
            headers={'Authorization': f'Bearer {tokenadmin}'},
        )

        assert response.status_code == 404
        assert 'detail' in response.json()


def test_delete_tipos_usuarios_exception_reassign_users_and_delete_tipo_usuario1(
    client, userTipoAdmin, tokenadmin
):
    with patch(
        'app.api.tipo_usuario.crud_tipo_usuario.reassign_users_and_delete_tipo_usuario'
    ) as mock_reassign:
        mock_reassign.side_effect = ObjectNotFoundException(
            'Tipo de usuário não encontrado', ''
        )

        response = client.delete(
            '/tipos_usuario/999',
            headers={'Authorization': f'Bearer {tokenadmin}'},
        )

        assert response.status_code == 404
        assert 'detail' in response.json()


def test_get_tipo_usuario_not_found(
    session, client, userTipoAdmin, tokenadmin
):
    id = 999

    with pytest.raises(ObjectNotFoundException):
        crud_tipo_user.get_tipo_usuario(session, tipo_usuario_id=id)


def test_delete_tipo_usuario_not_found(client):

    id = 999

    response = client.delete(f'/tipos_usuario/{id}')

    assert response.status_code == 404
    assert 'detail' in response.json()
