# executa os teste: pytest test/test_reserva.py

from datetime import datetime

from app.reserva.reserva_model import Reservation


def test_estrutura_do_banco_creat_reserva_adm(
    session, userTipoAdmin, userAdmin, AreaUserAdmin
):
    new_reservation = Reservation(
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
    session.add(new_reservation)
    session.commit()
    reserva = (
        session.query(Reservation)
        .filter(Reservation.reserva_tipo == 'Jogo')
        .first()
    )
    assert reserva.valor == 10
    assert reserva.reserva_data == datetime.strptime(
        '2023-10-23T12:00:00', '%Y-%m-%dT%H:%M:%S'
    )
    assert reserva.hora_inicio == datetime.strptime(
        '2023-10-23T14:00:00', '%Y-%m-%dT%H:%M:%S'
    )
    assert reserva.hora_fim == datetime.strptime(
        '2023-10-23T16:00:00', '%Y-%m-%dT%H:%M:%S'
    )
    assert reserva.justificacao == 'Jogo de Equipe'
    assert reserva.reserva_tipo == 'Jogo'
    assert reserva.status == 'Em análise'
    assert reserva.area_id == 1
    assert reserva.usuario_id == 1


def test_estrutura_do_banco_creat_reserva_cliente(
    session, userTipoClient, userCliente, AreaUserAdmin
):
    new_reservation = Reservation(
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
    session.add(new_reservation)
    session.commit()
    reserva = (
        session.query(Reservation)
        .filter(Reservation.justificacao == 'Jogo de Equipe Cliente')
        .first()
    )
    assert reserva.valor == 10
    assert reserva.reserva_data == datetime.strptime(
        '2023-10-23T16:00:00', '%Y-%m-%dT%H:%M:%S'
    )
    assert reserva.hora_inicio == datetime.strptime(
        '2023-10-23T17:00:00', '%Y-%m-%dT%H:%M:%S'
    )
    assert reserva.hora_fim == datetime.strptime(
        '2023-10-23T19:00:00', '%Y-%m-%dT%H:%M:%S'
    )
    assert reserva.justificacao == 'Jogo de Equipe Cliente'
    assert reserva.reserva_tipo == 'Jogo cliente'
    assert reserva.status == 'Em análise'
    assert reserva.area_id == 1
    assert reserva.usuario_id == 1


def test_create_reserva_adm(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    reserva_data = {
        'valor': 10,
        'reserva_data': '2023-10-23T12:00:00',
        'hora_inicio': '2023-10-23T14:00:00',
        'hora_fim': '2023-10-23T16:00:00',
        'justificacao': 'Jogo de Equipe',
        'reserva_tipo': 'Jogo',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userAdmin.id,
    }
    response = client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json()['valor'] == 20
    assert response.json()['reserva_data'] == '2023-10-23T12:00:00'
    assert response.json()['hora_inicio'] == '2023-10-23T14:00:00'
    assert response.json()['hora_fim'] == '2023-10-23T16:00:00'
    assert response.json()['justificacao'] == 'Jogo de Equipe'
    assert response.json()['reserva_tipo'] == 'Jogo'
    assert response.json()['status'] == 'Em análise'
    assert response.json()['area_id'] == AreaUserAdmin.id
    assert response.json()['usuario_id'] == userAdmin.id


def test_create_reserva_adm_fail_hora_indisponivel(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    # o valor sempre pode ser enviado como 0 pq o valor é calculado no backend
    reserva_data = {
        'valor': 10,
        'reserva_data': '2023-10-23T12:00:00',
        'hora_inicio': '2023-10-23T14:00:00',
        'hora_fim': '2023-10-23T16:00:00',
        'justificacao': 'Jogo de Equipe',
        'reserva_tipo': 'Jogo',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userAdmin.id,
    }
    response = client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'Horário indiponível para essa Área'


def test_create_reserva_cliente(
    client, userTipoClient, userCliente, AreaUserAdmin, tokencliente
):
    # o valor sempre pode ser enviado como 0 pq o valor é calculado no backend
    reserva_data = {
        'valor': 0,
        'reserva_data': '2023-10-23T16:00:00',
        'hora_inicio': '2023-10-23T17:00:00',
        'hora_fim': '2023-10-23T19:00:00',
        'justificacao': 'Jogo de Equipe Cliente',
        'reserva_tipo': 'Jogo cliente',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userCliente.id,
    }

    response = client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 200
    assert response.json()['valor'] == 20
    assert response.json()['reserva_data'] == '2023-10-23T16:00:00'
    assert response.json()['hora_inicio'] == '2023-10-23T17:00:00'
    assert response.json()['hora_fim'] == '2023-10-23T19:00:00'
    assert response.json()['justificacao'] == 'Jogo de Equipe Cliente'
    assert response.json()['reserva_tipo'] == 'Jogo cliente'
    assert response.json()['status'] == 'Em análise'
    assert response.json()['area_id'] == AreaUserAdmin.id
    assert response.json()['usuario_id'] == userCliente.id


def test_create_reserva_cliente_fail_horario_indisponivel(
    client,
    userTipoClient,
    userCliente,
    AreaUserAdmin,
    tokencliente,
    ReservaUserCliente,
):
    # o valor sempre pode ser enviado como 0 pq o valor é calculado no backend
    reserva_data = {
        'valor': 0,
        'reserva_data': '2023-10-23T16:00:00',
        'hora_inicio': '2023-10-23T17:00:00',
        'hora_fim': '2023-10-23T19:00:00',
        'justificacao': 'Jogo de Equipe Cliente',
        'reserva_tipo': 'Jogo cliente',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userCliente.id,
    }
    response = client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'Horário indiponível para essa Área'


def test_get_all_reservas(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    # esse teste pega a reserva que ja existe(ReservaUserAdmin) é a que é criada neste proprio teste
    reserva_data = {
        'valor': 0,
        'reserva_data': '2023-11-23T12:00:00',
        'hora_inicio': '2023-11-23T14:00:00',
        'hora_fim': '2023-11-23T16:00:00',
        'justificacao': 'Jogo de Equipe 2',
        'reserva_tipo': 'Jogo 2',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userAdmin.id,
    }
    client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    response = client.get('/reservas')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['id'] == 1
    assert response.json()[0]['valor'] == 10
    assert response.json()[0]['reserva_data'] == '2023-10-23T12:00:00'
    assert response.json()[0]['hora_inicio'] == '2023-10-23T14:00:00'
    assert response.json()[0]['hora_fim'] == '2023-10-23T16:00:00'
    assert response.json()[0]['justificacao'] == 'Jogo de Equipe'
    assert response.json()[0]['reserva_tipo'] == 'Jogo'
    assert response.json()[0]['status'] == 'Em análise'
    assert response.json()[0]['area_id'] == AreaUserAdmin.id
    assert response.json()[0]['usuario_id'] == userAdmin.id
    assert response.json()[1]['valor'] == 20
    assert response.json()[1]['id'] == 2
    assert response.json()[1]['reserva_data'] == '2023-11-23T12:00:00'
    assert response.json()[1]['hora_inicio'] == '2023-11-23T14:00:00'
    assert response.json()[1]['hora_fim'] == '2023-11-23T16:00:00'
    assert response.json()[1]['justificacao'] == 'Jogo de Equipe 2'
    assert response.json()[1]['reserva_tipo'] == 'Jogo 2'
    assert response.json()[1]['status'] == 'Em análise'
    assert response.json()[1]['area_id'] == AreaUserAdmin.id
    assert response.json()[1]['usuario_id'] == userAdmin.id


def test_get_reserva_by_id(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    response = client.get(
        f'/reservas/{ReservaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['valor'] == 10
    assert response.json()['reserva_data'] == '2023-10-23T12:00:00'
    assert response.json()['hora_inicio'] == '2023-10-23T14:00:00'
    assert response.json()['hora_fim'] == '2023-10-23T16:00:00'
    assert response.json()['justificacao'] == 'Jogo de Equipe'
    assert response.json()['reserva_tipo'] == 'Jogo'
    assert response.json()['status'] == 'Em análise'
    assert response.json()['area_id'] == AreaUserAdmin.id
    assert response.json()['usuario_id'] == userAdmin.id


def test_get_reserva_by_id_fail(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    response = client.get(
        '/reservas/3', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Reservation not found'


# FIXME: verificar o porque a rota do endpoint de update esta me retornando nada nesse update (como ele é 95% parecido com area que o teste de update dele esta funcionando....)
def test_update_reserva(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    reserva_data = {
        'valor': 0,
        'reserva_data': '2023-11-23T12:00:00',
        'hora_inicio': '2023-11-23T14:00:00',
        'hora_fim': '2023-11-23T16:00:00',
        'justificacao': 'Jogo de Equipe 2',
        'reserva_tipo': 'Jogo 2',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userAdmin.id,
    }
    response = client.put(
        f'/reservas/{ReservaUserAdmin.id}',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    # print(response.json())
    assert response.status_code == 200


def test_update_reserva_fail(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    reserva_data = {
        'valor': 0,
        'reserva_data': '2023-11-23T12:00:00',
        'hora_inicio': '2023-11-23T14:00:00',
        'hora_fim': '2023-11-23T16:00:00',
        'justificacao': 'Jogo de Equipe 2',
        'reserva_tipo': 'Jogo 2',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userAdmin.id,
    }
    response = client.put(
        '/reservas/3',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Reservation not found'


def test_delete_reserva(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    response = client.delete(
        f'/reservas/{ReservaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'Reserva deletada com sucesso'}


def test_delete_reserva_fail(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    response = client.delete(
        '/reservas/3', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'reserva not found'


def test_get_reservas_usuario(
    client,
    userTipoClient,
    userCliente,
    tokencliente,
    AreaUserAdmin,
    ReservaUserCliente,
):
    response = client.get(
        '/usuario/reservas',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == 1
    assert response.json()[0]['valor'] == 10


def test_get_reservas_usuario_fail(
    client,
    userTipoClient,
    userCliente,
    tokencliente,
    AreaUserAdmin,
    ReservaUserCliente,
):
    response = client.get('/usuario/reservas')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'
