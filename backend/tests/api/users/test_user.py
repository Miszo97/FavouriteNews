from fastapi import status
from queries.user_query import UserQuery
from tests.conftest import create_user


def test_get_user(authorized_client):
    response = authorized_client.get("/users/me")

    assert response.json().get("username") == "active_user"
    assert response.json().get("email") == "active_user@gmail.com"


def test_update_user(session, authorized_client):
    user = UserQuery().get_user_by_id(session, 1)

    assert user.id == 1
    assert user.username == "active_user"
    assert user.email == "active_user@gmail.com"

    data = {"username": "new_username", "email": "new_email"}

    response = authorized_client.patch("/users/me", json=data)

    assert response.json().get("username") == "new_username"
    assert response.json().get("email") == "new_email"
    assert response.json().get("hashed_password") != "plain_password"


def test_get_users(session, authorized_client):
    create_user(session, username="John", email="John@gmail.com", id=2)
    create_user(session, username="Ave", email="Ave@gmail.com", id=3)

    response = authorized_client.get("/users/me")

    assert len(response.json()) == 3


def test_get_users_unauthorized(session, client):
    create_user(session, username="John", email="John@gmail.com", id=2)
    create_user(session, username="Ave", email="Ave@gmail.com", id=3)

    response = client.get("/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
