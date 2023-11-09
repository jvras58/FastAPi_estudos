# executa os teste: pytest test/test_area.py

from app.area.area_model import Area


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
    assert response.status_code == 400
    assert response.json()['detail'] == 'Área já existe'


def test_create_area_cliente(
    client, userTipoClient, userCliente, tokencliente
):
    """
    Teste para criar uma area por um usuário cliente.
    a API retorna o erro 403 com a resposta 'Permissão negada. Somente administradores podem acessar esta rota.'

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
        == 'Permissão negada. Somente administradores podem acessar esta rota.'
    )


def test_get_all_areas(client, userTipoAdmin, AreaUserAdmin, tokenadmin):
    """
    Testa o endpoint de recuperar todas as areas disponiveis
    Verifica se a area foi criada+recuperada corretamente e se suas informações estão corretas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.

    """
    # esse teste pega a area que ja existe(AreaUserAdmin) é a que é criada neste proprio teste
    area_data = {
        'nome': 'Quadra de tênis',
        'descricao': 'Uma quadra de tênis espaçosa',
        'iluminacao': 'LED',
        'tipo_piso': 'Liso',
        'covered': 'Sim',
        'foto_url': 'https://example.com/quadra_tenis.jpg',
    }
    client.post(
        '/areas',
        json=area_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    response = client.get('/areas')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['nome'] == 'Quadra de volei'
    assert response.json()[0]['descricao'] == 'Uma quadra de volei espaçosa'
    assert response.json()[0]['iluminacao'] == 'LED'
    assert response.json()[0]['tipo_piso'] == 'Liso'
    assert response.json()[0]['covered'] == 'Sim'
    assert (
        response.json()[0]['foto_url']
        == 'https://example.com/quadra_volei.jpg'
    )
    assert response.json()[1]['nome'] == 'Quadra de tênis'
    assert response.json()[1]['descricao'] == 'Uma quadra de tênis espaçosa'
    assert response.json()[1]['iluminacao'] == 'LED'
    assert response.json()[1]['tipo_piso'] == 'Liso'
    assert response.json()[1]['covered'] == 'Sim'
    assert (
        response.json()[1]['foto_url']
        == 'https://example.com/quadra_tenis.jpg'
    )


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
    assert response.json()['detail'] == 'Area not found'


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
    assert response.json()['detail'] == 'Area not found'


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
    assert response.json()['detail'] == 'Area not found'


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
    assert response.json()['detail'] == 'Area not found'
