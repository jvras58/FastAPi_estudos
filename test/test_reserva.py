# executa os teste: pytest test/test_reserva.py
from datetime import datetime
from unittest.mock import patch

from app.api.reserva.reserva_model import Reservation
from app.utils.Exceptions.exceptions import ObjectNotFoundException


def test_delete_reservation_exception(client):
    """
    Testa se a exceção é lançada corretamente quando a reserva não é encontrada.
    """
    with patch(
        'app.api.reserva.crud_reserva.delete_reservation'
    ) as mock_delete_reservation:
        mock_delete_reservation.side_effect = ObjectNotFoundException(
            'Reserva não encontrada', ''
        )

        response = client.delete('/reserva/1')

        assert response.status_code == 404
        assert 'detail' in response.json()


def test_estrutura_do_banco_creat_reserva_adm(
    session, userTipoAdmin, userAdmin, AreaUserAdmin
):
    """
    Testa a criação de uma reserva por um cliente-administrador no banco de dados.

    Verifica se a reserva foi criado corretamente e se suas informações estão corretas.

    Args:
        session: objeto de sessão do SQLAlchemy.
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário do tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
    """
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
    """
    Testa a criação de uma reserva por um cliente no banco de dados.

    Verifica se a reserva foi criado corretamente e se suas informações estão corretas.

    Args:
        session: objeto de sessão do SQLAlchemy.
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário do tipo 'cliente'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
    """
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
    """
    Teste para criar uma reserva por um usuário administrador.
    Verifica se a reserva foi criada corretamente e se suas informações estão corretas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
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


# FIXME: Parou de funcionar por causa das mudanças no get_user_by_id para retornar um exception diretamente
def test_create_reserva_adm_fail_usuario_nao_existe(
    client, userTipoAdmin, AreaUserAdmin, tokenadmin
):
    """
    Teste para criar uma reserva por um usuário inexistente.
    Verifica se a API retorna o status code 404 e a mensagem de erro 'Usuario não existe ou não está autenticado'
    quando é feita uma requisição de criação da reserva é feita de um usuário que não existe na base de dados.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    reserva_data = {
        'valor': 10,
        'reserva_data': '2023-10-23T12:00:00',
        'hora_inicio': '2023-10-23T14:00:00',
        'hora_fim': '2023-10-23T16:00:00',
        'justificacao': 'Jogo de Equipe',
        'reserva_tipo': 'Jogo',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': 9999,
    }
    response = client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_create_reserva_adm_fail_area_nao_existe(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    """
    Teste para criar uma reserva por uma area inexistente.
    Verifica se a API retorna o status code 400 e a mensagem de erro 'Area não existe'
    quando é feita uma requisição de criação da reserva é feita de a partir de um id de area que não existe na base de dados.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    reserva_data = {
        'valor': 10,
        'reserva_data': '2023-10-23T12:00:00',
        'hora_inicio': '2023-10-23T14:00:00',
        'hora_fim': '2023-10-23T16:00:00',
        'justificacao': 'Jogo de Equipe',
        'reserva_tipo': 'Jogo',
        'status': 'Em análise',
        'area_id': 50,
        'usuario_id': userAdmin.id,
    }
    response = client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_create_reserva_adm_fail_hora_indisponivel(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    """
    Teste para criar uma reserva numa hora indisponivel.
    Verifica se a API retorna o status code 400 e a mensagem de erro 'Horário indiponível para essa Área'
    quando é feita uma requisição de criação da reserva é feita de a partir de um hora em que a area ja está sendo usada por outra reserva.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    # o valor sempre pode ser enviado como 0 pq o valor é calculado no endpoint
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
    assert 'conflict availability' in response.json()['detail'].lower()


def test_create_reserva_cliente(
    client, userTipoClient, userCliente, AreaUserAdmin, tokencliente
):
    """
    Teste para criar uma reserva por um usuário cliente.
    Verifica se a reserva foi criada corretamente e se suas informações estão corretas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
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


def test_create_reserva_cliente_fail_usuario_nao_existe(
    client, userTipoClient, userCliente, AreaUserAdmin, tokencliente
):
    """
    Teste para criar uma reserva por um usuário inexistente.
    Verifica se a API retorna o status code 404 e a mensagem de erro 'Usuario não existe ou não está autenticado'
    quando é feita uma requisição de criação da reserva é feita de um usuário que não existe na base de dados.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
    reserva_data = {
        'valor': 10,
        'reserva_data': '2023-10-23T12:00:00',
        'hora_inicio': '2023-10-23T14:00:00',
        'hora_fim': '2023-10-23T16:00:00',
        'justificacao': 'Jogo de Equipe',
        'reserva_tipo': 'Jogo',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': 9999,
    }
    response = client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 403
    assert 'conflict permission' in response.json()['detail'].lower()


# TODO: CRIAR UM TESTE ONDE UM ADM CONSIGA CRIAR UMA RESERVA PARA UM CLIENTE


def test_create_reserva_cliente_fail_area_nao_existe(
    client, userTipoClient, userCliente, tokencliente
):
    """
    Teste para criar uma reserva por uma area inexistente.
    Verifica se a API retorna o status code 400 e a mensagem de erro 'Area não existe'
    quando é feita uma requisição de criação da reserva é feita de a partir de um id de area que não existe na base de dados.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
    reserva_data = {
        'valor': 10,
        'reserva_data': '2023-10-23T12:00:00',
        'hora_inicio': '2023-10-23T14:00:00',
        'hora_fim': '2023-10-23T16:00:00',
        'justificacao': 'Jogo de Equipe',
        'reserva_tipo': 'Jogo',
        'status': 'Em análise',
        'area_id': 50,
        'usuario_id': userCliente.id,
    }
    response = client.post(
        '/reservas',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_create_reserva_cliente_fail_hora_indisponivel(
    client,
    userTipoClient,
    userCliente,
    AreaUserAdmin,
    tokencliente,
    ReservaUserCliente,
):
    """
    Teste para criar uma reserva numa hora indisponivel.
    Verifica se a API retorna o status code 400 e a mensagem de erro 'Horário indiponível para essa Área'
    quando é feita uma requisição de criação da reserva é feita de a partir de um hora em que a area ja está sendo usada por outra reserva.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que retorna um usuário do tipo 'cliente'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserCliente: fixture que retorna uma reserva criada por um usuário do tipo 'cliente'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
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
    assert 'conflict availability' in response.json()['detail'].lower()


def test_read_reservas(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    """
    Testa se é possível obter uma lista de RESERVAS.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
    """
    response = client.get('/reservas')
    assert response.status_code == 200
    assert len(response.json()['Reservation']) > 0


def test_read_reservas_not_found(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    tokenadmin,
):
    """
    Testa se é possível obter uma lista de RESERVAS.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
    """
    response = client.get('/reservas')
    assert response.status_code == 200
    assert 'Reservation' in response.json()


def test_get_reserva_adm_by_id(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    """
    Testa o endpoint de todas as reservas do usuario
    Verifica se o usuario pelo (ID) tem reservas vinculados ao seu ID além de criar uma nova reserva e verifica os dados de ambas reservas

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
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


def test_get_reserva_adm_by_id_fail_not_found(
    client, userTipoAdmin, userAdmin, AreaUserAdmin, tokenadmin
):
    response = client.get(
        '/reservas/3', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_update_reserva_adm(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    """
    Testa o endpoint de atualizar as reservas do usuario
    Verifica se a reserva pelo (ID) existe e verifica os dados de ambas reservas (nessa parte de verificar os dados da reserva esta dando falha)

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
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
    assert response.status_code == 200
    assert response.json()['valor'] == 20
    assert response.json()['reserva_data'] == '2023-11-23T12:00:00'
    assert response.json()['hora_inicio'] == '2023-11-23T14:00:00'
    assert response.json()['hora_fim'] == '2023-11-23T16:00:00'
    assert response.json()['justificacao'] == 'Jogo de Equipe 2'
    assert response.json()['reserva_tipo'] == 'Jogo 2'
    assert response.json()['status'] == 'Em análise'
    assert response.json()['area_id'] == AreaUserAdmin.id
    assert response.json()['usuario_id'] == userAdmin.id


def test_update_reserva_adm_fail_not_found(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    tokenadmin,
):
    """
    Testa o endpoint de atualizar as reservas do usuario
    Verifica se a reserva pelo (ID) existe como neste caso ela não existe ele retorna o status code 404 e a mensagem de erro 'Reservation not found'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
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
    assert 'not found' in response.json()['detail'].lower()


def test_update_reserva_cliente(
    client,
    userTipoClient,
    userCliente,
    AreaUserAdmin,
    ReservaUserCliente,
    tokencliente,
):
    """
    Testa o endpoint de atualizar as reservas do usuario
    Verifica se a reserva pelo (ID) existe e verifica os dados de ambas reservas (nessa parte de verificar os dados da reserva esta dando falha)

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    reserva_data = {
        'valor': 0,
        'reserva_data': '2023-11-23T12:00:00',
        'hora_inicio': '2023-11-23T14:00:00',
        'hora_fim': '2023-11-23T16:00:00',
        'justificacao': 'Jogo de Equipe 2',
        'reserva_tipo': 'Jogo 2',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userCliente.id,
    }
    response = client.put(
        f'/reservas/{ReservaUserCliente.id}',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 200
    assert response.json()['valor'] == 20
    assert response.json()['reserva_data'] == '2023-11-23T12:00:00'
    assert response.json()['hora_inicio'] == '2023-11-23T14:00:00'
    assert response.json()['hora_fim'] == '2023-11-23T16:00:00'
    assert response.json()['justificacao'] == 'Jogo de Equipe 2'
    assert response.json()['reserva_tipo'] == 'Jogo 2'
    assert response.json()['status'] == 'Em análise'
    assert response.json()['area_id'] == AreaUserAdmin.id
    assert response.json()['usuario_id'] == userCliente.id


def test_update_reserva_cliente_fail_not_found(
    client,
    userTipoClient,
    userCliente,
    AreaUserAdmin,
    tokencliente,
):
    """
    Testa o endpoint de atualizar as reservas do usuario
    Verifica se a reserva pelo (ID) existe como neste caso ela não existe ele retorna o status code 404 e a mensagem de erro 'Reservation not found'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    reserva_data = {
        'valor': 0,
        'reserva_data': '2023-11-23T12:00:00',
        'hora_inicio': '2023-11-23T14:00:00',
        'hora_fim': '2023-11-23T16:00:00',
        'justificacao': 'Jogo de Equipe 2',
        'reserva_tipo': 'Jogo 2',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userCliente.id,
    }
    response = client.put(
        '/reservas/3',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


# TODO: Refatorar essa rota para usuarios adm poderem atualizar reservas de outros usuarios
def test_update_reserva_cliente_fail_sem_permissao(
    client,
    userTipoAdmin,
    userAdmin,
    tokenadmin,
    userTipoClient,
    userCliente2,
    tokencliente,
    AreaUserAdmin,
    ReservaUserAdmin,
):
    """
    Testa o endpoint de atualizar as reservas do usuario
    Verifica se a reserva pelo (ID) existe e se o usuário tem permissão para atualizá-la.
    Neste caso, o usuário não tem permissão, então ele retorna o status code 403 e a mensagem de erro 'Sem permissão para atualizar a reserva.'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        userCliente: fixture que retorna um usuário tipo 'cliente'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
        tokencliente: token de autenticação JWT para o usuário cliente.
    """
    reserva_data = {
        'valor': 0,
        'reserva_data': '2023-11-23T12:00:00',
        'hora_inicio': '2023-11-23T14:00:00',
        'hora_fim': '2023-11-23T16:00:00',
        'justificacao': 'Jogo de Equipe 2',
        'reserva_tipo': 'Jogo 2',
        'status': 'Em análise',
        'area_id': AreaUserAdmin.id,
        'usuario_id': userCliente2.id,
    }
    response = client.put(
        f'/reservas/{ReservaUserAdmin.id}',
        json=reserva_data,
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 403
    assert (
        response.json()['detail']
        == 'Usuário não tem permissão para realizar essa ação'
    )


def test_delete_reserva_adm(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
):
    """
    Testa verificar se uma reserva pode ser excluída com sucesso.
    Verifica se a reserva pelo (ID) existe e se ela foi excluída com sucesso.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    response = client.delete(
        f'/reservas/{ReservaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'Reserva deletada com sucesso'}


# FIXME: CORRIGIR ROTA DE DELETE DE RESERVA POIS CLIENTE NÃO PODE DELETAR RESERVAS DE OUTROS CLIENTES SOMENTE ADMS
def test_delete_reserva_admin_passando_tokencliente(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
    tokenadmin,
    userTipoClient,
    userCliente,
    tokencliente,
):
    """
    Testa verificar se uma reserva pode ser excluída com sucesso.
    Verifica se a reserva pelo (ID) existe e se ela foi excluída com sucesso.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        ReservaUserAdmin: fixture que retorna uma reserva criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    response = client.delete(
        f'/reservas/{ReservaUserAdmin.id}',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 403
    assert 'detail' in response.json()


def test_delete_reserva_adm_fail_reserva_not_found(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    tokenadmin,
):
    """
    Testa o endpoint de atualizar as reservas do usuario
    Verifica se a reserva pelo (ID) existe como neste caso ela não existe ele retorna o status code 404 e a mensagem de erro 'Reservation not found'

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que retorna um usuário do tipo 'administrador'.
        userAdmin: fixture que retorna um usuário tipo 'administrador'.
        AreaUserAdmin: fixture que retorna uma área criada por um usuário do tipo 'administrador'.
        tokenadmin: token de autenticação JWT para o usuário administrador.
    """
    response = client.delete(
        '/reservas/3', headers={'Authorization': f'Bearer {tokenadmin}'}
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_get_reservas_usuario_cliente(
    client,
    userTipoClient,
    userCliente,
    tokencliente,
    AreaUserAdmin,
    ReservaUserCliente,
):
    """
    Testa a rota que retorna as reservas de um usuário. Verifica se a rota retorna o status code 200 e se o usuário tem uma reserva.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: fixture que cria um usuário do tipo cliente.
        userCliente: fixture que cria um usuário do tipo cliente.
        tokencliente: fixture que gera um token de acesso para o usuário cliente.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário admin.
        ReservaUserCliente: fixture que cria uma reserva para o usuário cliente.
    """
    response = client.get(
        '/usuario/reservas',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == 1
    assert response.json()[0]['valor'] == 10


def test_get_reservas_usuario_fail_Not_authenticated(
    client,
    userTipoClient,
    userCliente,
    tokencliente,
    AreaUserAdmin,
    ReservaUserCliente,
):
    """Testa se um usuário não autenticado recebe uma resposta 401 'Not authenticated' ao tentar acessar suas reservas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: O tipo de usuário do cliente.
        userCliente: O usuário cliente.
        tokencliente: O token de autenticação do cliente.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário admin.
        ReservaUserCliente: A reserva do usuário cliente.
    """
    response = client.get('/usuario/reservas')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'


def test_get_reservas_usuario_fail_Not_found(
    client,
    userTipoClient,
    userCliente,
    tokencliente,
    AreaUserAdmin,
):
    """Testa se um usuário não autenticado recebe uma resposta 401 'Not authenticated' ao tentar acessar suas reservas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: O tipo de usuário do cliente.
        userCliente: O usuário cliente.
        tokencliente: O token de autenticação do cliente.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário admin.
        ReservaUserCliente: A reserva do usuário cliente.
    """
    response = client.get(
        '/usuario/reservas',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_get_reservas_id_usuario_cliente(
    client,
    userTipoClient,
    tokencliente,
    AreaUserAdmin,
    ReservaUserCliente,
):
    """
    Testa a rota que retorna uma reserva específica de um usuário cliente autenticado e verifica os dados dessa reserva.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: O tipo de usuário do cliente.
        userCliente: O usuário cliente.
        tokencliente: O token de autenticação do cliente.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário(restrição para somente usuarios adms poderem criar as areas ativado).
        ReservaUserCliente: A reserva do usuário cliente.
    """
    response = client.get(
        f'/usuario/reservas/{ReservaUserCliente.id}',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['valor'] == 10


def test_get_reservas_id_usuario_cliente_fail_not_authenticated(
    client,
    userTipoClient,
    userCliente,
    AreaUserAdmin,
    ReservaUserCliente,
):
    """
    Testa se um usuário não autenticado recebe uma resposta 401 'Not authenticated' ao tentar acessar suas reservas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: O tipo de usuário do cliente.
        userCliente: O usuário cliente.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário(restrição para somente usuarios adms poderem criar as areas ativado).
        ReservaUserCliente: A reserva do usuário cliente.
    """
    response = client.get(
        f'/usuario/reservas/{ReservaUserCliente.id}',
    )
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'


def test_get_reservas_id_usuario_cliente_fail_not_found(
    client,
    userTipoClient,
    userCliente,
    tokencliente,
    AreaUserAdmin,
    ReservaUserCliente,
):
    """
    Testa se um usuário com um id de reserva inexistente recebe uma resposta 404 'Reservation not found' ao tentar acessar suas reservas.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoClient: O tipo de usuário do cliente.
        userCliente: O usuário cliente.
        tokencliente: O token de autenticação do cliente.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário(restrição para somente usuarios adms poderem criar as areas ativado).
        ReservaUserCliente: A reserva do usuário cliente.
    """
    response = client.get(
        '/usuario/reservas/3',
        headers={'Authorization': f'Bearer {tokencliente}'},
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_get_reservas_id_usuario_adm(
    client,
    userTipoAdmin,
    tokenadmin,
    AreaUserAdmin,
    ReservaUserCliente,
):
    """
    Testa a rota que retorna as reservas de um usuário. Verifica se a rota retorna o status code 200 e os dados do id da reserva é o valor

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que cria um usuário do tipo admin.
        userAdmin: fixture que cria um usuário do tipo admin.
        tokenadmin: fixture que gera um token de acesso para o usuário admin.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário admin.
        ReservaUserAdmin: fixture que cria uma reserva para o usuário admin.
    """
    response = client.get(
        f'/usuario/reservas/{ReservaUserCliente.id}',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['valor'] == 10


def test_get_reservas_id_usuario_adm_fail_not_authenticated(
    client,
    userTipoAdmin,
    userAdmin,
    AreaUserAdmin,
    ReservaUserAdmin,
):
    """
    Testa a rota que retorna as reservas de um usuário. Verifica se a rota retorna o status code 401 e a mensagem de erro 'Not authenticated' quando o usuário não está autenticado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que cria um usuário do tipo admin.
        userAdmin: fixture que cria um usuário do tipo admin.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário admin.
        ReservaUserAdmin: fixture que cria uma reserva para o usuário admin.
    """
    response = client.get(
        f'/usuario/reservas/{ReservaUserAdmin.id}',
    )
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'


def test_get_reservas_id_usuario_adm_fail_not_found(
    client,
    userTipoAdmin,
    tokenadmin,
    AreaUserAdmin,
    ReservaUserCliente,
):
    """
    Testa a rota que retorna as reservas de um usuário. Verifica se a rota retorna o status code 404 e a mensagem de erro 'Reservation not found' quando o usuário não está autenticado.

    Args:
        client: objeto cliente do test_client(FASTAPI).
        userTipoAdmin: fixture que cria um usuário do tipo admin.
        userAdmin: fixture que cria um usuário do tipo admin.
        tokenadmin: fixture que gera um token de acesso para o usuário admin.
        AreaUserAdmin: fixture que cria uma área de uso para o usuário admin.
        ReservaUserAdmin: fixture que cria uma reserva para o usuário admin.
    """
    response = client.get(
        '/usuario/reservas/3',
        headers={'Authorization': f'Bearer {tokenadmin}'},
    )
    assert response.status_code == 404
    assert 'not found' in response.json()['detail'].lower()


def test_get_reserva_usuario_fail_not_owner(
    client,
    userTipoClient,
    userCliente,
    tokencliente2,
    AreaUserAdmin,
    ReservaUserCliente,
):
    response = client.get(
        f'/usuario/reservas/{ReservaUserCliente.id}',
        headers={'Authorization': f'Bearer {tokencliente2}'},
    )
    assert response.status_code == 403
    assert 'conflict permission' in response.json()['detail'].lower()
