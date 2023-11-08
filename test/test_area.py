# executa os teste: pytest test/test_area.py

from app.area.area_model import Area


def test_estrutura_do_banco_creat_area(session, userTipoAdmin, userAdmin):
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


def test_get_all_areas(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
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


def test_get_area_by_name(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
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
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    response = client.get(f'/areas/nome/{AreaUserAdmin.iluminacao}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Area not found'


def test_get_area_by_id(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
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
    response = client.get(
        '/areas/3', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Area not found'


def test_update_area(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
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
    response = client.delete(
        f'/areas/{AreaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'Área deletada com sucesso'}


def test_delete_area_fail(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    response = client.delete(
        '/areas/3', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Area not found'
