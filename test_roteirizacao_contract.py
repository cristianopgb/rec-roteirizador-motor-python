from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_roteirizar_sem_blocos_obrigatorios_retorna_422():
    response = client.post('/roteirizar', json={})
    assert response.status_code == 422
