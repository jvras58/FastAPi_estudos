# executa os teste: pytest test/test_area.py


from app.api.area.area_model import Area


def test_estrutura_do_banco_creat_area(session, userTipoAdmin, userAdmin):
    """
    Testa a criação de uma area por um cliente-administrador no banco de dados.

    Verifica se a area foi criado corretamente e se suas informações estão corretas.

    Args:
        session: objeto de sessão do SQLAlchemy.
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário do tipo 'administrador'.
    """
    new_area = Area(
        nome='Quadra de volei',
        descricao='Uma quadra de volei espaçosa',
        iluminacao='LED',
        tipo_piso='Liso',
        covered='Sim',
        foto_url='https://example.com/quadra_volei.jpg',
    )
    session.add(new_area)
    session.commit()
    area = session.query(Area).filter(Area.nome == 'Quadra de volei').first()
    assert area.nome == 'Quadra de volei'
    assert area.descricao == 'Uma quadra de volei espaçosa'
    assert area.iluminacao == 'LED'
    assert area.tipo_piso == 'Liso'
    assert area.covered == 'Sim'
    assert area.foto_url == 'https://example.com/quadra_volei.jpg'


def test_create_area_adm(client, userTipoAdmin, userAdmin, tokenadmin):
    """
    Teste para criar uma area por um usuário administrador.
    Verifica se a area foi criada corretamente e se suas informações estão corretas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    area_data = {
        'nome': 'Quadra de volei',
        'descricao': 'Uma quadra de volei espaçosa',
        'iluminacao': 'LED',
        'tipo_piso': 'Liso',
        'covered': 'Sim',
        'foto_url': 'https://example.com/quadra_volei.jpg',
    }
    response = client.post(
        '/areas',
        json=area_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json()['nome'] == 'Quadra de volei'
    assert response.json()['descricao'] == 'Uma quadra de volei espaçosa'
    assert response.json()['iluminacao'] == 'LED'
    assert response.json()['tipo_piso'] == 'Liso'
    assert response.json()['covered'] == 'Sim'
    assert (
        response.json()['foto_url'] == 'https://example.com/quadra_volei.jpg'
    )


# TODO: MODELO DE COMO DEVE SER SEGUINDO O UM POUCO DO PADRÃO DE MARLOS
def test_create_area_adm_fail(
    client, userTipoAdmin, AreaUserAdmin, userAdmin, tokenadmin
):
    """
    Teste para criar uma area por um usuário administrador.
    a area não é criada pois já existe uma area com o mesmo nome é apresenta o erro 400 com a resposta 'Área já existe'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma area criada por um usuário administrador.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    area_data = {
        'nome': 'Quadra de volei',
        'descricao': 'Uma quadra de volei espaçosa',
        'iluminacao': 'LED',
        'tipo_piso': 'Liso',
        'covered': 'Sim',
        'foto_url': 'https://example.com/quadra_volei.jpg',
    }
    response = client.post(
        '/areas',
        json=area_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 409
    assert 'already exist with id' in response.json()['detail'].lower()


def test_create_area_cliente(
    client, userTipoClient, userCliente, tokencliente
):
    """
    Teste para criar uma area por um usuário cliente.
    a API retorna o erro 403 com a resposta 'Usuário não tem permissão para realizar essa ação'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
    area_data = {
        'nome': 'Quadra de volei',
        'descricao': 'Uma quadra de volei espaçosa',
        'iluminacao': 'LED',
        'tipo_piso': 'Liso',
        'covered': 'Sim',
        'foto_url': 'https://example.com/quadra_volei.jpg',
    }
    response = client.post(
        '/areas',
        json=area_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 403
    assert (
        response.json()['detail']
        == 'Usuário não tem permissão para realizar essa ação'
    )


def test_create_area_no_admin_exception(
    client, userTipoClient, userCliente, tokencliente
):
    """
    Teste para criar uma área por um usuário não administrador.
    A API deve retornar o erro 403 com a resposta 'Sem permissão para acessar essa rota.'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
    area_data = {
        'nome': 'Quadra de volei',
        'descricao': 'Uma quadra de volei espaçosa',
        'iluminacao': 'LED',
        'tipo_piso': 'Liso',
        'covered': 'Sim',
        'foto_url': 'https://example.com/quadra_volei.jpg',
    }
    response = client.post(
        '/areas',
        json=area_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 403
    assert (
        response.json()['detail']
        == 'Usuário não tem permissão para realizar essa ação'
    )


def test_read_areas(
    client, userTipoAdmin, userAdmin, tokenadmin, AreaUserAdmin
):
    """
    Testa se é possível obter uma lista de reservas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
    """
    response = client.get('/areas')
    assert response.status_code == 200
    assert len(response.json()['areas']) > 0


def test_read_areas_area_nao_existe(
    client, userTipoAdmin, userAdmin, tokenadmin
):
    """
    Testa se é possível obter uma lista de usuários.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
    """
    response = client.get('/areas')
    assert response.status_code == 200
    assert 'areas' in response.json()


def test_get_area_by_name(client, userTipoAdmin, AreaUserAdmin, tokenadmin):
    """
    Testa o endpoint de recuperar a area pelo nome
    Verifica se a area recuperada corretamente e se suas informações estão corretas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.

    """
    response = client.get(f'/areas/nome/{AreaUserAdmin.nome}')
    assert response.status_code == 200
    assert response.json()['nome'] == 'Quadra de volei'
    assert response.json()['descricao'] == 'Uma quadra de volei espaçosa'
    assert response.json()['iluminacao'] == 'LED'
    assert response.json()['tipo_piso'] == 'Liso'
    assert response.json()['covered'] == 'Sim'
    assert (
        response.json()['foto_url'] == 'https://example.com/quadra_volei.jpg'
    )
    assert response.json()['id'] == 1


# TODO: MODELO DE COMO DEVE SER SEGUINDO O UM POUCO DO PADRÃO DE MARLOS
def test_get_area_by_name_fail(
    client, userTipoAdmin, AreaUserAdmin, tokenadmin
):
    """
    Testa o endpoint de recuperar a area pelo nome mas a area não existe então retorna o erro 404 com a resposta 'Area not found'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.

    """
    response = client.get(f'/areas/nome/{AreaUserAdmin.iluminacao}')
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_get_area_by_id(client, userTipoAdmin, AreaUserAdmin, tokenadmin):
    """
    Testa o endpoint de recuperar a area pelo id
    Verifica se a area foi recuperada corretamente e se suas informações estão corretas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.

    """
    response = client.get(
        f'/areas/{AreaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json()['nome'] == 'Quadra de volei'
    assert response.json()['descricao'] == 'Uma quadra de volei espaçosa'
    assert response.json()['iluminacao'] == 'LED'
    assert response.json()['tipo_piso'] == 'Liso'
    assert response.json()['covered'] == 'Sim'
    assert (
        response.json()['foto_url'] == 'https://example.com/quadra_volei.jpg'
    )
    assert response.json()['id'] == 1


def test_get_area_by_id_fail(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    """
    Testa o endpoint de recuperar a area pelo id mas o id dessa area não existe então retorna o erro 404 com a resposta 'Area not found'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    response = client.get(
        '/areas/3', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_get_area_by_id_no_admin_exception(
    client, userTipoClient, AreaUserAdmin, tokencliente
):
    """
    Teste para obter uma área por ID por um usuário não administrador.
    A API deve retornar o erro 403 com a resposta 'Sem permissão para acessar essa rota.'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
    response = client.get(
        f'/areas/{AreaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 403
    assert (
        response.json()['detail']
        == 'Usuário não tem permissão para realizar essa ação'
    )


def test_update_area(client, userTipoAdmin, AreaUserAdmin, tokenadmin):
    """
    Testa o endpoint de atualizar a area
    Verifica se a area foi recuperada é verifica se as atualização estão corretas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    new_area = {
        'nome': 'Quadra de tenis',
        'descricao': 'Uma quadra de tenis espaçosa',
        'iluminacao': 'LED',
        'tipo_piso': 'Liso',
        'covered': 'Sim',
        'foto_url': 'https://example.com/quadra_tenis.jpg',
    }
    response = client.put(
        f'/areas/{AreaUserAdmin.id}',
        json=new_area,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json()['nome'] == 'Quadra de tenis'
    assert response.json()['descricao'] == 'Uma quadra de tenis espaçosa'
    assert response.json()['iluminacao'] == 'LED'
    assert response.json()['tipo_piso'] == 'Liso'
    assert response.json()['covered'] == 'Sim'
    assert (
        response.json()['foto_url'] == 'https://example.com/quadra_tenis.jpg'
    )


def test_update_area_not_admin(
    client, userTipoClient, AreaUserAdmin, tokencliente
):
    """
    Testa o endpoint de atualizar a area
    a api retorna o erro 403 com a resposta 'Usuário não tem permissão para realizar essa ação'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
    new_area = {
        'nome': 'Quadra de tenis',
        'descricao': 'Uma quadra de tenis espaçosa',
        'iluminacao': 'LED',
        'tipo_piso': 'Liso',
        'covered': 'Sim',
        'foto_url': 'https://example.com/quadra_tenis.jpg',
    }
    response = client.put(
        f'/areas/{AreaUserAdmin.id}',
        json=new_area,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 403
    assert (
        response.json()['detail']
        == 'Usuário não tem permissão para realizar essa ação'
    )


def test_update_area_fail(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    """
    Testa o endpoint de atualizar a area mas o id dessa area não existe então retorna o erro 404 com a resposta 'Area not found'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    new_area = {
        'nome': 'Quadra de tenis',
        'descricao': 'Uma quadra de tenis espaçosa',
        'iluminacao': 'LED',
        'tipo_piso': 'Liso',
        'covered': 'Sim',
        'foto_url': 'https://example.com/quadra_tenis.jpg',
    }
    response = client.put(
        '/areas/3',
        json=new_area,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_delete_area(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    """
    Testa o endpoint de deletar a area pelo id dessa area
    Verifica se a area foi deletada corretamente e se a resposta foi 'Área deletada com sucesso'.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    response = client.delete(
        f'/areas/{AreaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'Área deletada com sucesso'}


def test_delete_area_not_admin(
    client, userTipoClient, AreaUserAdmin, tokencliente
):
    """
    Testa o endpoint de deletar a area pelo id dessa area
    a api retorna o erro 403 com a resposta 'Usuário não tem permissão para realizar essa ação'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
    response = client.delete(
        f'/areas/{AreaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 403
    assert (
        response.json()['detail']
        == 'Usuário não tem permissão para realizar essa ação'
    )


def test_delete_area_fail(client, userTipoAdmin, AreaUserAdmin, tokenadmin):
    """
    Testa o endpoint de deletar a area pelo id mas o id dessa area não existe então retorna o erro 404 com a resposta 'Area not found'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    response = client.delete(
        '/areas/3', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()
