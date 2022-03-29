from models.user import User
from queries.user_query import UserQuery
from tests.conftest import create_user


def test_create_user(session):
    new_user = User(
        username="Mike", email="mike@gmail.com", hashed_password="fb34jkfsdf"
    )
    assert len(session.query(User).all()) == 0

    UserQuery().create_user(session, new_user)

    assert len(session.query(User).all()) == 1

    user = session.query(User).first()

    assert user.username == "Mike"


def test_get_users(session):
    create_user(session)
    create_user(session, username="Jon", email="John@gmail.com", id=2)
    create_user(session, username="Paul", email="Paul@gmail.com", id=3)

    users_qs = UserQuery().get_users(session)
    assert len(users_qs) == 3

    user_one = UserQuery().get_user_by_id(session, 2)
    assert user_one.username == "Jon"

    user_two = UserQuery().get_user_by_username(session, "Paul")
    assert user_two.email == "Paul@gmail.com"


def test_set_user_attribute(session, create_user_instance):
    user = UserQuery().set_email(session, 1, "newEmail@gmail.com")
    assert user.email == "newEmail@gmail.com"

    user = UserQuery().set_username(session, 1, "newUsername")
    assert user.username == "newUsername"
