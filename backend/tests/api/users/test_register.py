from fastapi import status
from passlib.context import CryptContext
from queries.user_query import UserQuery


def test_register_user(client, session):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    registration_form_1 = {
        "username": "Mike",
        "password": "secret",
        "email": "mike@gmail.com",
    }
    registration_form_2 = {
        "username": "John",
        "password": "top_secret",
        "email": "john@gmail.com",
    }

    expected_response_1 = {"id": 1, "username": "Mike", "email": "mike@gmail.com"}

    expected_response_2 = {"id": 2, "username": "John", "email": "john@gmail.com"}

    response = client.post("/users", data=registration_form_1)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response_1
    assert pwd_context.verify(
        "secret", UserQuery().get_users(session)[0].hashed_password
    )

    response = client.post("/users", data=registration_form_2)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response_2
    assert pwd_context.verify(
        "top_secret", UserQuery().get_users(session)[1].hashed_password
    )


def test_register_user_taken_username(client, session):
    registration_form_1 = {
        "username": "Mike",
        "password": "secret",
        "email": "mike@gmail.com",
    }
    registration_form_2 = {
        "username": "Mike",
        "password": "top_secret",
        "email": "john@gmail.com",
    }

    response = client.post("/users", data=registration_form_1)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/users", data=registration_form_2)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert len(UserQuery().get_users(session)) == 1


def test_register_user_taken_email(client, session):
    registration_form_1 = {
        "username": "Mike",
        "password": "secret",
        "email": "mike@gmail.com",
    }

    registration_form_2 = {
        "username": "Mikeee",
        "password": "top_secret",
        "email": "mike@gmail.com",
    }

    response = client.post("/users", data=registration_form_1)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/users", data=registration_form_2)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert len(UserQuery().get_users(session)) == 1


def test_register_user_missing_required_values(client, session):
    registration_form_no_username = {"password": "secret", "email": "mike@gmail.com"}
    registration_form_no_password = {"username": "Mike", "email": "mike@gmail.com"}
    registration_form_no_email = {"username": "Mike", "password": "secret"}

    response = client.post("/users", data=registration_form_no_username)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.post("/users", data=registration_form_no_password)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.post("/users", data=registration_form_no_email)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    assert len(UserQuery().get_users(session)) == 0
