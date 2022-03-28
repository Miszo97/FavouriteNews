import pytest
import sqlalchemy as sa
from app.main import app
from database import Base
from dependecies import get_db
from fastapi.testclient import TestClient

# we need this import for Base.metadata
from models.user import User  # noqa
from models.user_search_settings import UserSearchSettings  # noqa

from queries.user_query import UserQuery
from queries.user_serach_settings_query import UserSearchSettingsQuery
from schemas.user_schema import UserObject
from schemas.user_search_settings_schema import UserSearchSettingsObject
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@database:5432/test"

engine = sa.create_engine(SQLALCHEMY_DATABASE_URL)

if not database_exists(url=engine.url):
    create_database(engine.url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the database once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override as before, it uses the one provided by the
# session fixture.
@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture()
def create_user_instance(session):
    new_user = UserObject(
        username="Mike", email="mike@gmail.com", hashed_password="fb34jkfsdf", id=1
    )
    UserQuery().create_user(session, new_user)


@pytest.fixture()
def create_user_search_settings_instance(session):
    new_settings = UserSearchSettingsObject(
        country="Poland",
        category="Sport News",
        source="cnn",
        language="French",
        user_id=1,
        id=1,
    )
    UserSearchSettingsQuery().create_user_search_settings(session, new_settings)


@pytest.fixture()
def create_multiple_user_instances(session):
    new_user_one = UserObject(
        username="Mike", email="mike@gmail.com", hashed_password="fb34jkfsdf", id=1
    )
    new_user_two = UserObject(
        username="Bob", email="bob@gmail.com", hashed_password="sdsda4142", id=2
    )
    new_user_three = UserObject(
        username="John", email="john@gmail.com", hashed_password="dgij314saf", id=3
    )

    UserQuery().create_user(session, new_user_one)
    UserQuery().create_user(session, new_user_two)
    UserQuery().create_user(session, new_user_three)


@pytest.fixture()
def create_multiple_users_search_settings_instance(session):
    new_settings_one = UserSearchSettingsObject(
        country="Poland",
        category="Sport News",
        source="cnn",
        language="French",
        user_id=1,
        id=1,
    )
    new_settings_two = UserSearchSettingsObject(
        country="France",
        category="Health News",
        source="bbc",
        language="Portuguese",
        user_id=2,
        id=2,
    )
    new_settings_three = UserSearchSettingsObject(
        country="India",
        category="Sport News",
        source="cnn",
        language="Swedish",
        user_id=3,
        id=3,
    )

    UserSearchSettingsQuery().create_user_search_settings(session, new_settings_one)
    UserSearchSettingsQuery().create_user_search_settings(session, new_settings_two)
    UserSearchSettingsQuery().create_user_search_settings(session, new_settings_three)
