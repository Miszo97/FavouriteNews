from fastapi import status
from queries.user_query import UserQuery
from tests.conftest import create_user

user_query = UserQuery()


def test_get_user(authorized_client):
    response = authorized_client.get("/users/me")

    assert response.json().get("username") == "active_user"
    assert response.json().get("email") == "active_user@gmail.com"


def test_update_user(session, authorized_client):
    user = user_query.get_user_by_id(session, 1)

    assert user.id == 1
    assert user.username == "active_user"
    assert user.email == "active_user@gmail.com"

    data = {"username": "new_username", "email": "new_email"}

    response = authorized_client.patch("/users/me", json=data)

    assert len(UserQuery().get_users(session)) == 1
    updated_user = UserQuery().get_user_by_id(session, 1)

    assert response.json().get("id") == 1
    assert updated_user.id == 1

    assert response.json().get("username") == "new_username"
    assert updated_user.username == "new_username"

    assert response.json().get("email") == "new_email"
    assert updated_user.email == "new_email"

    assert response.json().get("hashed_password") != "plain_password"


def test_update_user_taken_username(session, authorized_client):
    user = user_query.get_user_by_id(session, 1)

    assert user.id == 1
    assert user.username == "active_user"
    assert user.email == "active_user@gmail.com"

    data = {"username": "active_user"}
    response = authorized_client.patch("/users/me", json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_user_taken_email(session, authorized_client):
    user = user_query.get_user_by_id(session, 1)

    assert user.id == 1
    assert user.username == "active_user"
    assert user.email == "active_user@gmail.com"

    data = {"email": "active_user@gmail.com"}
    response = authorized_client.patch("/users/me", json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_users(session, authorized_client):
    create_user(session, username="John", email="John@gmail.com", id=2)
    create_user(session, username="Ave", email="Ave@gmail.com", id=3)

    response = authorized_client.get("/users/me")

    assert len(response.json()) == 3


def test_delete_user(session, authorized_client):
    create_user(session, username="John", email="John@gmail.com", id=2)
    create_user(session, username="Ave", email="Ave@gmail.com", id=3)

    response = authorized_client.delete("/users/3")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(user_query.get_users(session)) == 2
    assert user_query.get_user_by_id(session, 3) is None


def test_delete_your_user(session, authorized_client):
    response = authorized_client.delete("/users/1")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(user_query.get_users(session)) == 1


def test_delete_unexisting_user(session, authorized_client):
    create_user(session, username="John", email="John@gmail.com", id=2)
    create_user(session, username="Ave", email="Ave@gmail.com", id=3)

    response = authorized_client.delete("/users/40")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}
    assert len(user_query.get_users(session)) == 3


def test_get_users_unauthorized(session, client):
    create_user(session, username="John", email="John@gmail.com", id=2)
    create_user(session, username="Ave", email="Ave@gmail.com", id=3)

    response = client.get("/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
