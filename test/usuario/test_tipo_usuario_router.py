from fastapi.testclient import TestClient
from database.get_db import SessionLocal, get_db
from app.area.crud_area import create_area
from app.tipo_usuario.tipo_usuario_controller import router_tipo_usuario


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