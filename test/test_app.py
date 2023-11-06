from fastapi.testclient import TestClient

from app.main import app

# executa os teste: pytest test/test_app.py


def test_root_deve_retornar_200_e_hello_world():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}
