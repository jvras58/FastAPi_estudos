
from fastapi.testclient import TestClient
from app.area.area_controller import router_area
from app.area.crud_area import get_area_by_name


def test_create_area_adm():
    client = TestClient(router_area)

    # Simulando dados de entrada
    area_data = {
        "id": "0e398c13-163c-4939-a68b-39b21e10c2c7",
        "nome": "Quadra de volei",
        "descricao": "Uma quadra de volei espaçosa",
        "iluminacao": "LED",
        "tipo_piso": "Liso",
        "covered": "Sim",
        "foto_url": "https://example.com/quadra_volei.jpg",
        "usuario_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
    }

    response = client.post('/areas', json=area_data)

    assert response.status_code == 200
    assert response.json() == {
        "id": "0e398c13-163c-4939-a68b-39b21e10c2c7", 
        "usuario_id": area_data["usuario_id"],
        "nome": area_data["nome"],
        "descricao": area_data["descricao"],
        "iluminacao": area_data["iluminacao"],
        "tipo_piso": area_data["tipo_piso"],
        "covered": area_data["covered"],
        "foto_url": area_data["foto_url"],
        "usuario_id": area_data["usuario_id"] 
    }

    area_criada = get_area_by_name(area_data["nome"])
    assert area_criada is not None
    assert area_criada.usuario_id == area_data["usuario_id"]


