from fastapi.testclient import TestClient

from src.app.core.config import settings
from src.app.main import app

from .helper import _get_token

test_name = settings.TEST_NAME
test_username = settings.TEST_USERNAME
test_email = settings.TEST_EMAIL
test_password = settings.TEST_PASSWORD

admin_username = settings.ADMIN_USERNAME
admin_password = settings.ADMIN_PASSWORD

client = TestClient(app)


# def test_post_customer(client: TestClient) -> None:
#     response = client.post(
#         "/api/v1/customer",
#         json={"customer_name": "Nguyen Ha Nam", "dob": "2000-06-20", "id_number": '036090193456', "address": '123 Elm Street, Springfield', 'credit_score': 850},
#     )
#     assert response.status_code == 201

# def test_update_customer(client: TestClient) -> None:
#     token = _get_token(username=test_username, password=test_password, client=client)

#     response = client.patch(
#         f"/api/v1/customer/{3}",
#         json={"customer_name": "Nguyen Nam Phuong", "dob": "2000-06-20", "id_number": '036090193456', "address": '123 Elm Street, Springfield', 'credit_score': 850},
#         headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
#     )
#     assert response.status_code == 200


# def test_delete_customer(client: TestClient) -> None:
#     token = _get_token(username= test_username, password= test_password, client=client)

#     response = client.delete(
#         f"/api/v1/customer/{2}", headers={"Authorization": f'Bearer {token.json()["access_token"]}'}
#     )
#     assert response.status_code == 200

def test_get_multiple_customers(client: TestClient) -> None:
    token = _get_token(username= test_username, password= test_password, client=client)
    response = client.get("/api/v1/customers",headers={"Authorization": f'Bearer {token.json()["access_token"]}'})
    assert response.status_code == 200



def test_get_customer(client: TestClient) -> None:
    token = _get_token(username= test_username, password= test_password, client=client)
    response = client.get(f"/api/v1/customer/{3}",headers={"Authorization": f'Bearer {token.json()["access_token"]}'})
    assert response.status_code == 200


