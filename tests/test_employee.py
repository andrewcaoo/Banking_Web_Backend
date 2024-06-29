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


# def test_post_employee(client: TestClient) -> None:
#     token = _get_token(username=test_username, password=test_password, client=client)
#     response = client.post(
#         "/api/v1/employee",
#         json={
#             "employee_name": "Hong Hanh",
#             "citizen_id": "036093002003",
#             "branch_id": None,
#             "dob": "2024-06-29",
#             "degree": 0,
#             "date_of_hire": "2024-06-29"
#             },
#         headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
#     )
#     assert response.status_code == 201

def test_get_multiple_employee(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)

    response = client.get("/api/v1/employees",headers={"Authorization": f'Bearer {token.json()["access_token"]}'},)
    assert response.status_code == 200



def test_get_employee(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)

    response = client.get(f"/api/v1/employee/{3}",headers={"Authorization": f'Bearer {token.json()["access_token"]}'},)
    assert response.status_code == 200



# def test_update_employee(client: TestClient) -> None:
#     token = _get_token(username=test_username, password=test_password, client=client)

#     response = client.patch(
#         f"/api/v1/employee/{3}",
#         json={
#             "employee_name": "Hong Hanh",
#             "citizen_id": "036093092003",
#             "branch_id": None,
#             "dob": "2024-06-29",
#             "degree": 0,
#             "date_of_hire": "2024-06-29"
#             },
#         headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
#     )
#     assert response.status_code == 200


# def test_delete_employee(client: TestClient) -> None:
#     token = _get_token(username= test_username, password= test_password, client=client)

#     response = client.delete(
#         f"/api/v1/employee/{2}", headers={"Authorization": f'Bearer {token.json()["access_token"]}'}
#     )
#     assert response.status_code == 200

