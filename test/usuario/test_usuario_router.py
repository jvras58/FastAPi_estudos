from fastapi.testclient import TestClient

# teste para as rotas de usuario
from app.tipo_usuario.tipo_usuario_controller import router_tipo_usuario

# teste para as rotas de usuario
from app.usuario.usuario_controller import router_usuario


def test_create_tipo_usuario_adm():
    client = TestClient(router_tipo_usuario)

    # Simulando dados de entrada
    tipo_usuario_data = {
        "id": "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b",
        "tipo": "administrador"
    }

    response = client.post("/tipos_usuario", json=tipo_usuario_data)

    assert response.status_code == 200
    assert response.json()["id"] == "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b"
    assert response.json()["tipo"] == "administrador"

def test_create_usuario():
    client = TestClient(router_usuario)
    # Simulando dados de entrada
    usuario_data = {
        "id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b",
        "nome": "Jonh test",
        "tipo_id": "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b",
        "email": "john.test@example.com",
        "senha": "senha"
    }

    response = client.post("/usuarios", json=usuario_data)

    assert response.status_code == 200
    assert response.json()["id"] == "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
    assert response.json()["nome"] == "Jonh test"
    assert response.json()["tipo_id"] == "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b"
    assert response.json()["email"] == "john.test@example.com"
    assert response.json()["senha"] == "senha"

# CHECKING: verificar se teste funciona msm kk 
def test_login_for_access_token():
    client = TestClient(router_usuario)

    form_data = {
        "usarname": "john.test@example.com",
        "password": "senha"
    }

    # form_data = {
    #     "email": "john.test@example.com",
    #     "senha": "senha"
    # }

    response = client.post("/token", data=form_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_get_user():
    client = TestClient(router_usuario)

    # Simulando dados de entrada
    usuario_data_adm = {
        "id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b",
        "nome": "Jonh test",
        "tipo_id": "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b",
        "email": "john.test@example.com",
        "senha": "senha"
    }

    response_create_user = client.post("/usuarios", json=usuario_data_adm)
    user_id = response_create_user.json()["id"]

    response = client.get(f"/usuarios/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
    assert response.json()["nome"] == "Jonh test"
    assert response.json()["tipo_id"] == "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b"
    assert response.json()["email"] == "john.test@example.com"
    assert response.json()["senha"] == "senha"

def test_update_user():
    client = TestClient(router_usuario)

    # Simulando dados
    usuario_data_adm = {
        "id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b",
        "nome": "Jonh test",
        "tipo_id": "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b",
        "email": "john.test@example.com",
        "senha": "senha"
    }

    response_create_user = client.post("/usuarios", json=usuario_data_adm)
    user_id = response_create_user.json()["id"]

    # Simulando dados de atualização
    usuario_data_update = {
        "nome": "Jonh test 1",
        "email": "john.testjr@example.com",
        "senha": "senha123"
    }

    response_update_user = client.put(f"/usuarios/{user_id}", json=usuario_data_update)

    assert response_update_user.status_code == 200
    assert response_update_user.json()["id"] == user_id
    assert response_update_user.json()["nome"] == "Jonh test 1"
    assert response_update_user.json()["email"] == "john.testjr@example.com"
    assert response_update_user.json()["senha"] == "senha123"


def test_delete_user():
    client = TestClient(router_usuario)

    # Simulando dados de entrada
    usuario_data_adm = {
        "id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b",
        "nome": "Jonh test",
        "tipo_id": "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b",
        "email": "john.test@example.com",
        "senha": "senha"
    }

    response_create_user = client.post("/usuarios", json=usuario_data_adm)
    user_id = response_create_user.json()["id"]

    response_delete_user = client.delete(f"/usuarios/{user_id}")

    assert response_delete_user.status_code == 200
    assert response_delete_user.json() == {"detail": "Usuário deletado com sucesso"}

