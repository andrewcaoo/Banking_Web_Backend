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


# def test_post_acc(client: TestClient) -> None:
#     response = client.post(
#         "/api/v1/base_account",
#         json={"username": "abc", "email": "minh.a@gmail.com", "password": '123456', "employee_id": None, "cus_account_id": None, "profile_image_url": None, "is_ban": False, "permission": 0},
#     )
#     assert response.status_code == 201

def test_get_multiple_acc(client: TestClient) -> None:
    response = client.get("/api/v1/base_account")
    assert response.status_code == 200



def test_get_acc(client: TestClient) -> None:
    response = client.get(f"/api/v1/base_account/{test_username}")
    assert response.status_code == 200



# def test_update_user(client: TestClient) -> None:
#     token = _get_token(username=test_username, password=test_password, client=client)

#     response = client.patch(
#         f"/api/v1/base_account/{test_username}",
#         json={
#                 "username": test_username,
#                 "profile_image_url": "https://i.sstatic.net/l60Hf.png",
#                 "password": None,
#                 "permission": 0,
#                 "email": "user.userson@example.com",
#                 "employee_id": None,
#                 "cus_account_id": None,
#                 "is_ban": True,
#                 "is_deleted": False
#                 },
#         headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
#     )
#     assert response.status_code == 200


# def test_delete_user(client: TestClient) -> None:
#     token = _get_token(username= test_username, password= test_password, client=client)

#     response = client.delete(
#         f"/api/v1/base_account/{test_username}", headers={"Authorization": f'Bearer {token.json()["access_token"]}'}
#     )
#     assert response.status_code == 200

