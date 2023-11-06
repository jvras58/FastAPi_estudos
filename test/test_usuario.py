from dados_teste import DadosTeste_usuario
from sqlalchemy import select

# from app.tipo_usuario.tipo_usuario_controller import router_tipo_usuario
from app.usuario.usuario_model import TipoUser as tipo
from app.usuario.usuario_model import Usuario
from app.usuario.usuario_model import Usuario as User

# executa os teste: pytest test/test_usuario.py

def test_creat_tipo_adm(session):
    tipo_user = tipo(
        id=1,
        tipo='administrador',
    )
    session.add(tipo_user)
    session.commit()
    session.refresh(tipo_user)
    user = session.scalar(select(tipo).where(tipo.tipo == 'administrador'))
    assert user.tipo == 'administrador'


def test_creat_tipo_cliente(session):
    tipo_user = tipo(
        id=2,
        tipo='cliente',
    )
    session.add(tipo_user)
    session.commit()
    session.refresh(tipo_user)
    user = session.scalar(select(tipo).where(tipo.tipo == 'cliente'))
    assert user.tipo == 'cliente'


def test_creat_userAdmin(session, userTipoAdmin):
    new_user = Usuario(
        nome='adm test',
        tipo_id=1,
        email='adm.test@example.com',
        senha='senhaadm',
    )
    session.add(new_user)
    session.commit()
    user = session.query(Usuario).filter(Usuario.nome == 'adm test').first()
    #versão das querys de marlos 
    #user = session.scalar(select(Usuario).where(Usuario.nome == 'adm test'))
    assert user.nome == 'adm test'


def test_creat_userCliente(session, userTipoClient):
    new_user = Usuario(
        nome='cliente test',
        tipo_id=2,
        email='cliente.test@example.com',
        senha='senhacliente',
    )
    session.add(new_user)
    session.commit()
    user = session.scalar(
        select(Usuario).where(Usuario.nome == 'cliente test')
    )
    assert user.nome == 'cliente test'


def test_create_tipo_usuario_adm(client):
    tipo_usuario_data_adm = DadosTeste_usuario.tipo_usuario_adm()
    response = client.post('/tipos_usuario', json=tipo_usuario_data_adm)
    assert response.status_code == 200
    assert response.json() == tipo_usuario_data_adm

def test_create_tipo_usuario_cliente(client):
    tipo_usuario_data_cliente = DadosTeste_usuario.tipo_usuario_cliente()
    response = client.post('/tipos_usuario', json=tipo_usuario_data_cliente)
    assert response.status_code == 200
    assert response.json() == tipo_usuario_data_cliente

# como eu pego essa senha criptografada
def test_create_usuario_adm(client, userTipoAdmin):
    usuario_data = DadosTeste_usuario.usuario_adm()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 200
    # o problema do assert abaixo é pq a senha vira um token esquisito
    # assert response.json() == usuario_data

# como eu pego essa senha criptografada
def test_create_usuario_cliente(client, userTipoClient):
    usuario_data = DadosTeste_usuario.usuario_cliente()
    response = client.post('/usuarios', json=usuario_data)
    assert response.status_code == 200
    # o problema do assert abaixo é pq a senha vira um token esquisito
    # assert response.json() == usuario_data

# como eu pego essa senha criptografada
def test_get_user_adm(client, userTipoAdmin):

    new_user = {
        'nome': 'Marlos',
        'email': 'marlos@ufpe.br',
        'senha': 'qwe123',
        'tipo_id': 1,
    }
    response = client.post('/usuarios', json=new_user)
    assert response.status_code == 200
    # assert response.json() == new_user

# como eu pego essa senha criptografada
def test_get_user_cliente(client, userTipoClient):

    new_user = {
        'nome': 'jvras',
        'email': 'jvras@ufpe.br',
        'senha': '1234',
        'tipo_id': 2,
    }
    response = client.post('/usuarios', json=new_user)
    print(response.json())
    assert response.status_code == 200
    #assert response.json() == new_user


# ------------------------------------------- token sem funcionar pq não sei como pegar o token inicio --------------------------------------- #
# rotas de validar token do usuario /token:

# teste sem funcionar o status code esta vindo 422 tenho que descobrir como pego o hash da senha do codigo

# def test_login_for_access_token_adm(client, userTipoAdmin, userAdmin):
#     #form_data = DadosTeste_usuario.login_token_adm()
#     response = client.post('/token' )
#     assert 422 == 200
#     assert response.status_code == 200
#     assert 'access_token' in response.json()
#     assert response.json()['token_type'] == 'bearer'


# def test_login_for_access_token_cliente(client):
#     form_data = DadosTeste_usuario.login_token_cliente()
#     response = client.post('/token', data=form_data)
#     assert response.status_code == 200
#     assert 'access_token' in response.json()
#     assert response.json()['token_type'] == 'bearer'

# ------------------------------------------- token fim ---------------------------------------------------------------------------- #



def test_get_user_admin(client, userTipoAdmin, userAdmin):
    response = client.get(f'/usuarios/{userAdmin.id}')
    assert response.status_code == 200

# falha se so tentarmos mudar um parametro(tipo somente o nome): assert 422 == 200
def test_update_user_adm(client,userTipoAdmin, userAdmin):
    # tem algo de errado nessa rota? se o usuario so quiser mudar o nome... ele é obrigado a colocar os dados antigos todos? ai e foda kkk
    usuario_data_update = {'nome': 'adm test 1','tipo_id':1,'email':'adm.test@example.com','senha':'senhaadm',}
    response_update_user = client.put(
        f'/usuarios/{userAdmin.id}', json=usuario_data_update
    )
    assert response_update_user.status_code == 200


# esse em especifico eu não preciso do id mas preciso da autenticação
def test_delete_user_adm(client,userTipoAdmin, userAdmin):
    user_id = userAdmin.id
    # (preciso de um jeito de simular a autenticação ou pegar o token do usuario)
    # preciso pegar o token é colocar no headers outro modelo é headers={'Authorization': f'Bearer {token}'}
    response_delete_user = client.delete(
        f'/usuario/delete', headers={'Authorization': 'Bearer Token'}
    )
    # assert 401 == 200
    assert response_delete_user.status_code == 200
    assert response_delete_user.json() == {
        'detail': 'Usuário deletado com sucesso'
    }