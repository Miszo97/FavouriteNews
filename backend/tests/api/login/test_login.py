from fastapi import status
from models.user import User
from passlib.context import CryptContext
from queries.user_query import UserQuery


def test_user_correct_credentials(client, session):
    user_query = UserQuery()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    new_user = User(
        username="johndoe",
        email="johndoe@example.com",
        hashed_password=pwd_context.hash("secret"),
    )
    user_query.create_user(session, new_user)

    user_form = {"username": new_user.username, "password": "secret"}

    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert "access_token" in response_json


def test_user_incorrect_credentials(client, session):
    user_query = UserQuery()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    new_user = User(
        username="johndoe",
        email="johndoe@example.com",
        hashed_password=pwd_context.hash("secret"),
    )
    user_query.create_user(session, new_user)

    user_form = {"username": new_user.username, "password": "secreto"}

    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
