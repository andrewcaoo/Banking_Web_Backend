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


# def test_post_branch(client: TestClient) -> None:
#     token = _get_token(username= test_username, password= test_password, client=client)
#     response = client.post(
#         "/api/v1/branch",
#         json={"branch_name": "Tay Ho Ha Noi", "region_id": None, "employee_id": None, "open_date": "2000-06-20", 'open_hour': 8, 'close_hour': 18},
#         headers={"Authorization": f'Bearer {token.json()["access_token"]}'}
#     )
#     assert response.status_code == 201


def test_get_multiple_branch(client: TestClient) -> None:
    token = _get_token(username= test_username, password= test_password, client=client)
    response = client.get("/api/v1/branches",headers={"Authorization": f'Bearer {token.json()["access_token"]}'})
    assert response.status_code == 200



def test_get_branch(client: TestClient) -> None:
    token = _get_token(username= test_username, password= test_password, client=client)
    response = client.get(f"/api/v1/branch/{6}",headers={"Authorization": f'Bearer {token.json()["access_token"]}'})
    assert response.status_code == 200



# def test_update_branch(client: TestClient) -> None:
#     token = _get_token(username=test_username, password=test_password, client=client)

#     response = client.patch(
#         f"/api/v1/branch/{7}",
#         json={"branch_name": "Tay Ho Ha Noi", "region_id": None, "employee_id": None, "open_date": "2000-06-20", 'open_hour': 8, 'close_hour': 18},
#         headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
#     )
#     assert response.status_code == 200


# def test_delete_branch(client: TestClient) -> None:
#     token = _get_token(username= test_username, password= test_password, client=client)

#     response = client.delete(
#         f"/api/v1/branch/{7}", headers={"Authorization": f'Bearer {token.json()["access_token"]}'}
#     )
#     assert response.status_code == 200

