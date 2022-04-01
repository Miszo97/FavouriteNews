from fastapi import status
from models import User
from passlib.context import CryptContext


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
    }

    expected_response_1 = {"id": 1, "username": "Mike", "email": "mike@gmail.com"}

    expected_response_2 = {"id": 2, "username": "John", "email": None}

    response = client.post("users", data=registration_form_1)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response_1
    assert pwd_context.verify("secret", session.query(User).all()[0].hashed_password)

    response = client.post("users", data=registration_form_2)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response_2
    assert pwd_context.verify(
        "top_secret", session.query(User).all()[1].hashed_password
    )


def test_register_user_missing_required_values(client, session):
    registration_form_no_username = {"password": "secret", "email": "mike@gmail.com"}
    registration_form_no_password = {"username": "Mike", "email": "mike@gmail.com"}

    response = client.post("users", data=registration_form_no_username)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.post("users", data=registration_form_no_password)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    assert len(session.query(User).all()) == 0
