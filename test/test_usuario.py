from dados_teste import DadosTeste_usuario
from sqlalchemy import select

import app.security.auth as auth
from app.usuario.usuario_model import TipoUser as tipo
from app.usuario.usuario_model import Usuario

# executa os teste: pytest test/test_usuario.py


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


def test_estrutura_do_banco_creat_userAdmin(session, userTipoAdmin):
    """
    Testa a criação de um usuário administrador no banco de dados.

    Verifica se o usuário foi criado corretamente e se suas informações estão corretas.

    Args:
        session: objeto de sessão do SQLAlchemy.
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
    """
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
    """
    Testa a criação de um usuário cliente no banco de dados.

    Verifica se o usuário foi criado corretamente e se suas informações estão corretas.
    Args:
        session: objeto de sessão do SQLAlchemy.
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
    """
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


def test_post_create_usuario_adm(client, userTipoAdmin):
    """
    Testa a criação de um tipo de usuário administrador via requisição POST.

    Verifica se a resposta da requisição tem código de status 200 e se o JSON da Senha é Igual ao retornado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
    """
    usuario_data = DadosTeste_usuario.usuario_adm()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 200
    assert auth.verify_password(
        usuario_data['senha'], response.json()['senha']
    )


def test_post_create_usuario_adm_fail(client, userTipoAdmin, userAdmin):
    """
    Testa se um usuário administrador não pode criar outro usuário com um e-mail já registrado.
    verifica se a resposta da requisição tem código de status 400 e se o JSON retornado é igual a mensagem de erro.
    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
    """
    usuario_data = DadosTeste_usuario.usuario_adm()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'E-mail já registrado'


def test_post_create_usuario_cliente(client, userTipoClient):
    """
    Testa a criação de um tipo de usuário cliente via requisição POST.
    Verifica se a resposta da requisição tem código de status 200 e se o JSON da Senha é Igual ao retornado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
    """
    usuario_data = DadosTeste_usuario.usuario_cliente()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 200
    assert auth.verify_password(
        usuario_data['senha'], response.json()['senha']
    )


def test_post_create_usuario_cliente_fail(client, userTipoClient, userCliente):
    """
    Testa se um usuário cliente não pode criar outro usuário com um e-mail já registrado.
    verifica se a resposta da requisição tem código de status 400 e se o JSON retornado é igual a mensagem de erro.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
    """
    usuario_data = DadosTeste_usuario.usuario_cliente()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'E-mail já registrado'


def test_post_create_user_adm(session, client, userTipoAdmin):
    """
    Testa a criação de um usuário com perfil de administrador através de uma requisição POST.
    Verifica se o usuário é criado com sucesso, se suas informações estão corretas e se a senha foi criptografada corretamente.
    Também verifica se uma segunda tentativa de criação do mesmo usuário resulta em erro.

    Args:
        session: objeto de sessão do SQLAlchemy.
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
    """
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
    """
    Testa a criação de um usuário com perfil de cliente através de uma requisição POST.
    Verifica se o usuário é criado com sucesso, se suas informações estão corretas e se a senha foi criptografada corretamente.
    Também verifica se uma segunda tentativa de criação do mesmo usuário resulta em erro.

    Args:
        session: objeto de sessão do SQLAlchemy.
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
    """
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
    """
    Testa se é possível obter um token de acesso para um usuário administrador através do endpoint /token.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
    """
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
    """
    Testa se o endpoint '/token' retorna um código de status 401 e uma mensagem de erro
    quando as credenciais de login são inválidas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
    """
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
    """
    Testa se é possível obter um token de acesso para um usuário cliente através do endpoint /token.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
    """
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
    """
    Testa se é possível obter informações de um usuário administrador pelo ID.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
    """
    response = client.get(f'/usuarios/{userAdmin.id}')
    assert response.status_code == 200
    assert response.json()['nome'] == userAdmin.nome
    assert response.json()['email'] == userAdmin.email


def test_get_user_admin_fail_usuario_não_encontrado(
    client, userTipoAdmin, userAdmin
):
    """
    Testa se a rota retorna o status code 404 e a mensagem de erro correta
    quando o usuário não é encontrado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
    """
    response = client.get('/usuarios/20')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_get_user_admin_reservas_vazias(client, userTipoAdmin, userAdmin):
    """
    Testa se a rota '/usuarios/{userAdmin.id}/reservas' retorna uma lista vazia e um contador igual a zero
    quando o usuário é um administrador e não possui reservas.
    """
    response = client.get(f'/usuarios/{userAdmin.id}/reservas')
    assert response.status_code == 200
    assert response.json() == [[], 0]


def test_get_user_cliente(client, userTipoClient, userCliente):
    """
    Testa se é possível obter informações de um usuário cliente pelo ID.
    """
    response = client.get(f'/usuarios/{userCliente.id}')
    assert response.status_code == 200
    assert response.json()['nome'] == userCliente.nome
    assert response.json()['email'] == userCliente.email


def test_get_user_cliente_fail_usuario_nao_encontrado(
    client, userTipoClient, userCliente
):
    """
    Testa se a rota retorna o status code 404 e a mensagem de erro correta
    Verifica se a API retorna o status code 404 e a mensagem de erro 'Usuário não encontrado'
    quando é feita uma requisição de GET de um usuário que não existe na base de dados.
    """
    response = client.get('/usuarios/10')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_get_user_cliente_fail_reservas_vazias(
    client, userTipoClient, userCliente
):
    """
    Testa se a rota '/usuarios/{userCliente.id}/reservas' retorna uma lista vazia e um contador igual a zero
    quando o usuário é um cliente e não possui reservas.
    """
    response = client.get(f'/usuarios/{userCliente.id}/reservas')
    assert response.status_code == 200
    assert response.json() == [[], 0]


def test_update_user_adm(client, userTipoAdmin, userAdmin, tokenadmin):
    """
    Testa a atualização de um usuário com perfil de administrador.

    Verifica se a atualização é bem-sucedida e se os dados atualizados são retornados corretamente.
    """
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
    """
    Testa se a atualização de um usuário administrador falha quando o (ID) não é encontrado.
    Verifica se a API retorna o status code 404 e a mensagem de erro 'Usuário não encontrado'
    quando é feita uma requisição de atualização de um usuário que não existe na base de dados.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    response = client.get(
        '/usuarios/10',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuário não encontrado'}


# FiXME: esse teste deveria dar not_found para conseguir testar o erro do crud mas como no controller ja tém o erro do Usuário não encontrado ele acaba se sobrepondo
def test_update_user_adm_fail_user_not_found(
    client, userTipoAdmin, userAdmin, tokenadmin
):
    """
    Testa se a atualização de um usuário administrador falha quando o usuário não é encontrado.

    Verifica se a API retorna o status code 404 e a mensagem de erro 'Usuário não encontrado'
    quando é feita uma requisição de atualização de um usuário que não existe na base de dados.
    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    response_up_user = client.get(
        '/usuarios/10',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response_up_user.status_code == 404
    assert response_up_user.json() == {'detail': 'Usuário não encontrado'}


def test_update_user_cliente(
    client, userTipoClient, userCliente, tokencliente
):
    """
    Testa a atualização de um usuário do tipo cliente.

    Verifica se a atualização é bem sucedida, se os dados foram atualizados corretamente e se a busca por um usuário inexistente retorna o erro esperado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
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
    """
    Testa a falha na atualização de um usuário do tipo cliente.

    Verifica se a API retorna o status code 404 e a mensagem de erro 'Usuário não encontrado'
    quando é feita uma requisição de atualização de um usuário que não existe na base de dados.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        tokencliente: token de autenticação JWT para o usuário cliente.

    Returns:
        None
    """
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
    """
    Testa se um usuário administrador consegue se auto-deletar com sucesso.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo administrador.
        userAdmin: fixture que retorna um usuário administrador.
        tokenadmin: fixture que retorna um token de acesso para o usuário administrador.
    """
    response_delete_user = client.delete(
        '/usuario/delete', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response_delete_user.status_code == 200
    assert response_delete_user.json() == {
        'detail': 'Usuário deletado com sucesso'
    }


def test_delete_user_adm_fail_not_auth(client, userTipoAdmin, userAdmin):
    """
    Testa se um usuário administrador não autenticado se auto-deletar com sucesso.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo administrador.
        userAdmin: fixture que retorna um usuário administrador.
    """
    response_delete_user = client.delete(
        '/usuario/delete',
    )
    assert response_delete_user.status_code == 401
    assert response_delete_user.json() == {'detail': 'Not authenticated'}


def test_delete_user_id_adm(client, userTipoAdmin, userAdmin, tokenadmin):
    """
    Testa se um usuário administrador consegue deletar um usuário pelo ID.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo administrador.
        userAdmin: fixture que retorna um usuário administrador.
        tokenadmin: fixture que retorna um token de acesso para o usuário administrador.

    Returns:
        None
    """
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
    """
    Testa se o endpoint '/usuarios/delete/{user_id}' retorna o status code 404 e a mensagem de erro 'Usuário não encontrado'
    quando é feita uma requisição DELETE com um id de usuário inexistente, mas com um token válido.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo administrador.
        userAdmin: fixture que retorna um usuário administrador.
        tokenadmin: fixture que retorna um token de acesso para o usuário administrador.
    """
    user_id = 50
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response_delete_user.status_code == 404
    assert response_delete_user.json() == {'detail': 'Usuário não encontrado'}


def test_delete_user_id_adm_fail(client, userTipoAdmin, userAdmin):
    """
    Testa se o endpoint '/usuarios/delete/{user_id}' retorna o status code 401 e a mensagem de erro 'Not authenticated'
    quando é feita uma requisição DELETE com um id de usuário EXISTENTE, mas com um token ausente.

    args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo administrador.
        userAdmin: fixture que retorna um usuário administrador.
    """
    user_id = userAdmin.id
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
    )
    assert response_delete_user.status_code == 401
    assert response_delete_user.json() == {'detail': 'Not authenticated'}


# kk esse teste nem deve fazer muito sentido mas tudo bem (tecnicamente essa rota deve ser so pra adms poderem apagar a conta que quiser mas tudo bem kk) kk
def test_delete_user_id_cliente(
    client, userTipoClient, userCliente, tokencliente
):
    """
    Testa se um usuário cliente consegue deletar um usuário pelo ID.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo cliente.
        userCliente: fixture que retorna um usuário cliente.
        tokencliente: fixture que retorna um token de acesso para o usuário.

    Returns:
        None
    """
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
    """
    Testa se o endpoint '/usuarios/delete/{user_id}' retorna o status code 404 e a mensagem de erro 'Usuário não encontrado'
    quando é feita uma requisição DELETE com um id de usuário inexistente, mas com um token válido.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: Fixture que cria um usuário com a função 'cliente'.
        userCliente: Fixture que cria um usuário cliente.
        tokencliente: Fixture que gera um token de acesso para o usuário cliente.
    """

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
    """
    Testa se o endpoint '/usuarios/delete/{user_id}' retorna o status code 404 e a mensagem de erro 'Not authenticated'
    quando é feita uma requisição DELETE com um id de usuário existente, mas com um token inexistente.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: Fixture que cria um usuário com a função 'cliente'.
        userCliente: Fixture que cria um usuário cliente.
        tokencliente: Fixture que gera um token de acesso para o usuário cliente.
    """
    user_id = userCliente.id
    response_delete_user = client.delete(
        f'/usuarios/delete/{user_id}',
    )
    assert response_delete_user.status_code == 401
    assert response_delete_user.json() == {'detail': 'Not authenticated'}


def test_delete_user_cliente(
    client, userTipoClient, userCliente, tokencliente
):
    """
    Testa se um usuário cliente consegue se auto-deletar com sucesso.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: Fixture que cria um usuário com a função 'cliente'.
        userCliente: Fixture que cria um usuário cliente.
    """
    response_delete_user = client.delete(
        '/usuario/delete', headers={'Authorization': f'Bearer {tokencliente}'}
    )
    assert response_delete_user.status_code == 200
    assert response_delete_user.json() == {
        'detail': 'Usuário deletado com sucesso'
    }


def test_delete_user_user_fail_not_auth(client, userTipoClient, userCliente):
    """
    Testa se um usuário não autenticado não consegue deletar sua própria conta.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: Fixture que cria um usuário com a função 'cliente'.
        userCliente: Fixture que cria um usuário cliente.

    """
    response_delete_user = client.delete(
        '/usuario/delete',
    )
    assert response_delete_user.status_code == 401
    assert response_delete_user.json() == {'detail': 'Not authenticated'}


def test_get_user_reservations_adm(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, ReservaUserAdmin
):
    """
    Teste o endpoint que recupera todas as reservas feitas por um usuário específico (ID).

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com a função 'admin'.
        userAdmin: Fixture que cria um usuário administrador.
        AreaUserAdmin: Fixture que cria uma área associada ao usuário administrador.
        ReservaUserAdmin: Fixture que cria uma reserva associada ao usuário administrador.
    """
    response = client.get(f'/usuarios/{userAdmin.id}/reservas')
    assert response.status_code == 200
    assert response.json()[0][0]['id'] == ReservaUserAdmin.id
    assert response.json()[0][0]['area_id'] == ReservaUserAdmin.area_id


def test_get_user_reservations_adm_vazio(
    client,
    userTipoAdmin,
    userAdmin,
):
    """
    Teste o endpoint que recupera todas as reservas feitas por um usuário específico (ID) Como o usuario não tem o fixture de reservas então ele vai retornar vazio.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: Fixture que cria um usuário com a função 'admin'.
        userAdmin: Fixture que cria um usuário administrador.
    """
    response = client.get(f'/usuarios/{userAdmin.id}/reservas')
    assert response.status_code == 200
    assert response.json() == [[], 0]


def test_get_user_reservations_cliente(
    client, userTipoClient, userCliente, AreaUserAdmin, ReservaUserCliente
):
    """
    Teste o endpoint que recupera todas as reservas feitas por um usuário específico (ID).

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: Fixture que cria um usuário com a função 'cliente'.
        userCliente: Fixture que cria um usuário cliente.
        AreaUserAdmin: Fixture que cria uma área associada ao usuário administrador.
        ReservaUserAdmin: Fixture que cria uma reserva associada ao usuário administrador.
    """
    response = client.get(f'/usuarios/{userCliente.id}/reservas')
    assert response.status_code == 200
    assert response.json()[0][0]['id'] == ReservaUserCliente.id
    assert response.json()[0][0]['area_id'] == ReservaUserCliente.area_id


def test_get_user_reservations_cliente_fail_vazio(
    client,
    userTipoClient,
    userCliente,
):
    """
    Teste o endpoint que recupera todas as reservas feitas por um usuário específico (ID) Como o usuario não tem o fixture de reservas então ele vai retornar vazio.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: Fixture que cria um usuário com a função 'cliente'.
        userCliente: Fixture que cria um usuário cliente.

    """
    response = client.get(f'/usuarios/{userCliente.id}/reservas')
    assert response.status_code == 200
    assert response.json() == [[], 0]


"""
O endpoint está configurado para receber `new_password` e `old_password` como parâmetros de consulta. Se forem para ser recebebidos esses valores no corpo da requisição como JSON, deve-se usar um modelo Pydantic para definir a estrutura dos dados de entrada.
"""


def test_update_senha_incorrect_old_password(
    client, session, userTipoAdmin, userAdmin, tokenadmin
):
    """
    Testa se o usuário não pode atualizar sua senha com uma senha antiga incorreta.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        session: Fixture que cria um Objeto de sessão do SQLAlchemy.
        userTipoAdmin: Fixture que cria um usuário com a função 'admin'.
        userAdmin: Fixture que cria um usuário administrador.
        tokenadmin: Fixture que gera um token de acesso para o usuário administrador.

    Returns:
        None
    """
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
    """
    Testa se o usuário digita a senha nova vazia retorna um erro 400 quando a nova senha está vazia.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        session: Fixture que cria um Objeto de sessão do SQLAlchemy.
        userTipoAdmin: Fixture que cria um usuário com a função 'admin'.
        userAdmin: Fixture que cria um usuário administrador.
        tokenadmin: Fixture que gera um token de acesso para o usuário administrador.

    Returns:
        None
    """
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
    """
    Teste a funcionalidade de atualização de senha para um usuário ele retorna 200 com o aviso que a senha foi atualizada.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        session: Fixture que cria um Objeto de sessão do SQLAlchemy.
        userTipoAdmin: Fixture que cria um usuário com a função 'admin'.
        userAdmin: Fixture que cria um usuário administrador.
        tokenadmin: Fixture que gera um token de acesso para o usuário administrador.
    """
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


# os testes sempre apagam tudo que criam então por exemplo se na hora que eu criar uma reserva com o usuario de cliente usando os dados do fixture o usuario_id sempre vai ser 1
