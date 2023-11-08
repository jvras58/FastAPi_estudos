from dados_teste import DadosTeste_usuario
from sqlalchemy import select

import app.security.auth as auth
from app.usuario.usuario_model import TipoUser as tipo
from app.usuario.usuario_model import Usuario

# executa os teste: pytest test/test_usuario.py


def test_estrutura_do_banco_creat_tipo_adm(session):
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
    tipo_user = tipo(
        id=2,
        tipo='cliente',
    )
    session.add(tipo_user)
    session.commit()
    session.refresh(tipo_user)
    user = session.scalar(select(tipo).where(tipo.tipo == 'cliente'))
    assert user.tipo == 'cliente'


def test_estrutura_do_banco_creat_userAdmin(session, userTipoAdmin):
    clr_password = 'senhaadm'
    new_user = Usuario(
        nome='adm test',
        tipo_id=userTipoAdmin.id,
        email='adm.test@example.com',
        senha=auth.get_password_hash(clr_password),
    )
    session.add(new_user)
    session.commit()
    Usuario.clear_password = clr_password
    user = session.query(Usuario).filter(Usuario.nome == 'adm test').first()
    assert user.nome == 'adm test'
    assert auth.verify_password(clr_password, user.senha)
    assert user.tipo_id == 1
    assert user.email == 'adm.test@example.com'


def test_estrutura_do_banco_creat_userCliente(session, userTipoClient):
    clr_password = 'senhacliente'
    new_user = Usuario(
        nome='cliente test',
        tipo_id=userTipoClient.id,
        email='cliente.test@example.com',
        senha=auth.get_password_hash(clr_password),
    )
    session.add(new_user)
    session.commit()
    Usuario.clear_password = clr_password
    user = session.scalar(
        select(Usuario).where(Usuario.nome == 'cliente test')
    )
    assert user.nome == 'cliente test'
    assert user.tipo_id == 2
    assert user.email == 'cliente.test@example.com'
    assert auth.verify_password(clr_password, user.senha)


def test_post_create_tipo_usuario_adm(client):
    tipo_usuario_data_adm = DadosTeste_usuario.tipo_usuario_adm()
    response = client.post('/tipos_usuario', json=tipo_usuario_data_adm)
    assert response.status_code == 200
    assert response.json() == tipo_usuario_data_adm


def test_post_create_tipo_usuario_cliente(client):
    tipo_usuario_data_cliente = DadosTeste_usuario.tipo_usuario_cliente()
    response = client.post('/tipos_usuario', json=tipo_usuario_data_cliente)
    assert response.status_code == 200
    assert response.json() == tipo_usuario_data_cliente


def test_post_create_usuario_adm(client, userTipoAdmin):
    usuario_data = DadosTeste_usuario.usuario_adm()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 200
    assert auth.verify_password(
        usuario_data['senha'], response.json()['senha']
    )


def test_post_create_usuario_adm_fail(client, userTipoAdmin, userAdmin):
    usuario_data = DadosTeste_usuario.usuario_adm()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'E-mail já registrado'


def test_post_create_usuario_cliente(client, userTipoClient):
    usuario_data = DadosTeste_usuario.usuario_cliente()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 200
    assert auth.verify_password(
        usuario_data['senha'], response.json()['senha']
    )


def test_post_create_usuario_cliente_fail(client, userTipoClient, userCliente):
    usuario_data = DadosTeste_usuario.usuario_cliente()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'E-mail já registrado'


def test_post_create_user_adm(session, client, userTipoAdmin):
    clr_password = 'qwe123'
    new_user = {
        'nome': 'Marlos',
        'tipo_id': userTipoAdmin.id,
        'email': 'marlos@ufpe.br',
        'senha': clr_password,
    }
    response = client.post('/usuarios', json=new_user)
    assert response.status_code == 200
    user = session.scalar(select(Usuario).where(Usuario.nome == 'Marlos'))
    assert user.nome == 'Marlos'
    assert user.email == 'marlos@ufpe.br'
    pwd_hash = user.senha
    assert auth.verify_password(clr_password, pwd_hash)
    # esse eu deixei junto pq não tenho esse usuario dentro do fixture sorry chefinho
    response = client.post('/usuarios', json=new_user)
    assert response.status_code == 400
    assert response.json()['detail'] == 'E-mail já registrado'


def test_post_create_user_cliente(session, client, userTipoClient):
    clr_password = '1234'
    new_user = {
        'nome': 'jvras',
        'email': 'jvras@ufpe.br',
        'senha': clr_password,
        'tipo_id': userTipoClient.id,
    }
    response = client.post('/usuarios', json=new_user)
    assert response.status_code == 200
    user = session.scalar(select(Usuario).where(Usuario.nome == 'jvras'))
    assert user.nome == 'jvras'
    assert user.email == 'jvras@ufpe.br'
    pwd_hash = user.senha
    assert auth.verify_password(clr_password, pwd_hash)
    # esse eu deixei junto pq não tenho esse usuario dentro do fixture
    response = client.post('/usuarios', json=new_user)
    assert response.status_code == 400
    assert response.json()['detail'] == 'E-mail já registrado'


def test_post_login_for_access_token_adm(client, userTipoAdmin, userAdmin):
    response = client.post(
        '/token',
        data={
            'username': userAdmin.email,
            'password': userAdmin.clear_password,
        },
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'


def test_post_login_for_access_token_returns_unauthorized(
    client, userTipoAdmin, userAdmin
):
    response = client.post(
        '/token',
        data={
            'username': 'usuario_invalido',
            'password': 'senha_invalida',
        },
    )
    assert response.status_code == 401
    assert response.headers['WWW-Authenticate'] == 'Bearer'
    assert response.json()['detail'] == 'Incorrect username or password'


def test_post_login_for_access_token_cliente(
    client, userTipoClient, userCliente
):
    response = client.post(
        '/token',
        data={
            'username': userCliente.email,
            'password': userCliente.clear_password,
        },
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'


def test_get_user_admin(client, userTipoAdmin, userAdmin):
    response = client.get(f'/usuarios/{userAdmin.id}')
    assert response.status_code == 200
    assert response.json()['nome'] == userAdmin.nome
    assert response.json()['email'] == userAdmin.email


def test_get_user_admin_fail_usuario_não_encontrado(
    client, userTipoAdmin, userAdmin
):
    response = client.get('/usuarios/20')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_get_user_admin_reservas_vazias(client, userTipoAdmin, userAdmin):
    response = client.get(f'/usuarios/{userAdmin.id}/reservas')
    assert response.status_code == 200
    assert response.json() == [[], 0]


def test_get_user_cliente(client, userTipoClient, userCliente):
    response = client.get(f'/usuarios/{userCliente.id}')
    assert response.status_code == 200
    assert response.json()['nome'] == userCliente.nome
    assert response.json()['email'] == userCliente.email


def test_get_user_cliente_fail_usuario_nao_encontrado(
    client, userTipoClient, userCliente
):
    response = client.get('/usuarios/10')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_get_user_admin_fail_reservas_vazias(client, userTipoAdmin, userAdmin):
    response = client.get(f'/usuarios/{userAdmin.id}/reservas')
    assert response.status_code == 200
    assert response.json() == [[], 0]


def test_update_user_adm(client, userTipoAdmin, userAdmin, tokenadmin):
    usuario_data_update = {
        'nome': 'adm test 1',
        'tipo_id': 1,
        'email': 'adm.test@example.com',
        'senha': 'senhaadm',
    }
    response_update_user = client.put(
        f'/usuarios/{userAdmin.id}',
        json=usuario_data_update,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response_update_user.status_code == 200
    assert response_update_user.json()['nome'] == usuario_data_update['nome']
    assert response_update_user.json()['email'] == usuario_data_update['email']


def test_update_user_adm_fail_usuario_nao_encontrado(
    client, userTipoAdmin, userAdmin, tokenadmin
):
    usuario_data_update = {
        'nome': 'adm test 1',
        'tipo_id': 1,
        'email': 'adm.test@example.com',
        'senha': 'senhaadm',
    }
    response = client.get(
        '/usuarios/10',
        params=usuario_data_update,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user_adm_fail_user_not_found(
    client, userTipoAdmin, userAdmin, tokenadmin
):
    response_up_user = client.get(
        '/usuarios/10',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response_up_user.status_code == 404
    assert response_up_user.json() == {'detail': 'Usuário não encontrado'}


def test_update_user_cliente(
    client, userTipoClient, userCliente, tokencliente
):
    usuario_data_update = {
        'nome': 'cliente test 1',
        'tipo_id': 2,
        'email': 'cliente.test@example.com',
        'senha': 'senhacliente',
    }
    response_update_user = client.put(
        f'/usuarios/{userCliente.id}',
        json=usuario_data_update,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response_update_user.status_code == 200
    assert response_update_user.json()['nome'] == usuario_data_update['nome']
    assert response_update_user.json()['email'] == usuario_data_update['email']
    response = client.get('/usuarios/10')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user_cliente_fail(
    client, userTipoClient, userCliente, tokencliente
):
    usuario_data_update = {
        'nome': 'cliente test 1',
        'tipo_id': 2,
        'email': 'cliente.test@example.com',
        'senha': 'senhacliente',
    }
    response = client.get(
        '/usuarios/10',
        params=usuario_data_update,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_delete_user_adm(client, userTipoAdmin, userAdmin, tokenadmin):
    response_delete_user = client.delete(
        '/usuario/delete', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response_delete_user.status_code == 200
    assert response_delete_user.json() == {
        'detail': 'Usuário deletado com sucesso'
    }


def test_delete_user_adm_fail_not_auth(
    client, userTipoAdmin, userAdmin, tokenadmin
):
    response_delete_user = client.delete(
        '/usuario/delete',
    )
    assert response_delete_user.status_code == 401
    assert response_delete_user.json() == {'detail': 'Not authenticated'}


def test_delete_user_id_adm(client, userTipoAdmin, userAdmin, tokenadmin):
    user_id = userAdmin.id
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response_delete_user.status_code == 200
    assert response_delete_user.json() == {
        'detail': 'Usuário deletado com sucesso'
    }


def test_delete_user_id_adm_nao_encontrado(
    client, userTipoAdmin, userAdmin, tokenadmin
):
    user_id = 50
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response_delete_user.status_code == 404
    assert response_delete_user.json() == {'detail': 'Usuário não encontrado'}


def test_delete_user_id_adm_fail(client, userTipoAdmin, userAdmin, tokenadmin):
    user_id = userAdmin.id
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
    )
    assert response_delete_user.status_code == 401
    assert response_delete_user.json() == {'detail': 'Not authenticated'}


def test_delete_user_id_cliente(
    client, userTipoClient, userCliente, tokencliente
):
    user_id = userCliente.id
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response_delete_user.status_code == 200
    assert response_delete_user.json() == {
        'detail': 'Usuário deletado com sucesso'
    }


def test_delete_user_id_cliente_nao_encontrado(
    client, userTipoClient, userCliente, tokencliente
):
    user_id = 50
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response_delete_user.status_code == 404
    assert response_delete_user.json() == {'detail': 'Usuário não encontrado'}


def test_delete_user_id_cliente_fail_not_auth(
    client, userTipoClient, userCliente, tokencliente
):
    user_id = userCliente.id
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
    )
    assert response_delete_user.status_code == 401
    assert response_delete_user.json() == {'detail': 'Not authenticated'}


def test_delete_user_cliente(
    client, userTipoClient, userCliente, tokencliente
):
    response_delete_user = client.delete(
        '/usuario/delete', headers={'Authorization': f'Bearer {tokencliente}'}
    )
    assert response_delete_user.status_code == 200
    assert response_delete_user.json() == {
        'detail': 'Usuário deletado com sucesso'
    }


def test_delete_user_user_fail_not_auth(client, userTipoClient, userCliente):
    response_delete_user = client.delete(
        '/usuario/delete',
    )
    assert response_delete_user.status_code == 401
    assert response_delete_user.json() == {'detail': 'Not authenticated'}


"""
O endpoint está configurado para receber `new_password` e `old_password` como parâmetros de consulta. Se forem para ser recebebidos esses valores no corpo da requisição como JSON, deve-se usar um modelo Pydantic para definir a estrutura dos dados de entrada.
"""


def test_update_senha_incorrect_old_password(
    client, session, userTipoAdmin, userAdmin, tokenadmin
):
    new_password = 'new_password'
    old_password = 'incorrect_password'
    headers = {'Authorization': f'Bearer {tokenadmin}'}
    response = client.put(
        f'/usuario/update_senha?new_password={new_password}&old_password={old_password}',
        headers=headers,
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Senha antiga incorreta'}
    user = session.scalar(select(Usuario).where(Usuario.id == userAdmin.id))
    assert not auth.verify_password(new_password, user.senha)


def test_update_senha_empty_new_password(
    client, session, userTipoAdmin, userAdmin, tokenadmin
):
    new_password = ''
    old_password = userAdmin.clear_password
    headers = {'Authorization': f'Bearer {tokenadmin}'}
    response = client.put(
        f'/usuario/update_senha?new_password={new_password}&old_password={old_password}',
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Nova senha não pode ser vazia'}
    user = session.scalar(select(Usuario).where(Usuario.id == userAdmin.id))
    assert not auth.verify_password(new_password, user.senha)


def test_update_senha_success(
    client, session, userTipoAdmin, userAdmin, tokenadmin
):
    new_password = 'new_password'
    old_password = userAdmin.clear_password
    headers = {'Authorization': f'Bearer {tokenadmin}'}
    response = client.put(
        f'/usuario/update_senha?new_password={new_password}&old_password={old_password}',
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'Senha atualizada com sucesso'}
    user = session.scalar(select(Usuario).where(Usuario.id == userAdmin.id))
    assert auth.verify_password(new_password, user.senha)


def test_get_user_reservations_adm(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, ReservaUserAdmin
):
    response = client.get(f'/usuarios/{userAdmin.id}/reservas')
    assert response.status_code == 200
    assert response.json()[0][0]['id'] == ReservaUserAdmin.id
    assert response.json()[0][0]['area_id'] == ReservaUserAdmin.area_id


def test_get_user_reservations_adm_fail_vazio(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
):
    response = client.get(f'/usuarios/{userAdmin.id}/reservas')
    assert response.status_code == 200
    assert response.json() == [[], 0]


def test_get_user_reservations_cliente(
    client, userTipoClient, userCliente, AreaUserAdmin, ReservaUserCliente
):
    response = client.get(f'/usuarios/{userCliente.id}/reservas')
    assert response.status_code == 200
    assert response.json()[0][0]['id'] == ReservaUserCliente.id
    assert response.json()[0][0]['area_id'] == ReservaUserCliente.area_id


def test_get_user_reservations_cliente_fail_vazio(
    client,
    userTipoClient,
    userCliente,
    AreaUserAdmin,
):
    response = client.get(f'/usuarios/{userCliente.id}/reservas')
    assert response.status_code == 200
    assert response.json() == [[], 0]


# os testes sempre apagam tudo que criam então por exemplo se na hora que eu criar uma reserva com o usuario de cliente usando os dados do fixture o usuario_id sempre vai ser 1
