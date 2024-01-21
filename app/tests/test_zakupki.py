from fastapi.testclient import TestClient

def test_get_new(ac: TestClient):
    response = ac.get('/zakupki/get_data')
    assert response.status_code == 200