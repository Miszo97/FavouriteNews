from app.main import app
from fastapi.testclient import TestClient
from queries.user_query import UserQuery
from tests.conftest import create_user

client = TestClient(app)


def test_get_user(client, authorized_client):

    authorization = {"Authorization": "Bearer " + authorized_client.token}

    response = client.get("/users/me", headers=authorization)

    assert response.json().get("username") == "active_user"
    assert response.json().get("email") == "active_user@gmail.com"


def test_update_user(client, session, authorized_client):

    authorization = {"Authorization": "Bearer " + authorized_client.token}

    user = UserQuery().get_user_by_id(session, 1)

    assert user.id == 1
    assert user.username == "active_user"
    assert user.email == "active_user@gmail.com"

    data = {"username": "new_username", "email": "new_email"}

    response = client.patch("/users/me", headers=authorization, json=data)

    assert response.json().get("username") == "new_username"
    assert response.json().get("email") == "new_email"
    assert response.json().get("hashed_password") != "plain_password"


def test_get_users(client, session, authorized_client):
    create_user(session, username="John", email="John@gmail.com", id=2)
    create_user(session, username="Ave", email="Ave@gmail.com", id=3)

    authorization = {"Authorization": "Bearer " + authorized_client.token}
    response = client.get("/users/me/", headers=authorization)

    assert len(response.json()) == 3
