import pytest
import sqlalchemy as sa
from app.main import app
from database import Base
from dependecies import get_db
from enums import Category, Country, Language, Source
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


def create_user(
    session,
    username="Bob",
    email="Bob@example.com",
    hashed_password="erwsfd32431dsa",
    id=1,
    **extra
):
    user = UserObject(
        id=id,
        username=username,
        email=email,
        hashed_password=hashed_password,
    )

    user_db = UserQuery().create_user(session, user)
    return user_db


@pytest.fixture()
def create_user_search_settings_instance(session):
    new_settings = UserSearchSettingsObject(
        country=Country.PL,
        category=Category.GENERAL,
        source=Source.BBC,
        language=Language.DE,
        user_id=1,
        id=1,
    )
    UserSearchSettingsQuery().create_user_search_settings(session, new_settings)


def create_user_serach_settings(
    session,
    country=Country.PL,
    category=Category.BUSINESS,
    source=Source.CNN,
    language=Language.FR,
    user_id=1,
    id=1,
    **extra
):
    user_settings = UserSearchSettingsObject(
        country=country,
        category=category,
        source=source,
        language=language,
        user_id=user_id,
        id=id,
        **extra
    )
    user_settings_db = UserSearchSettingsQuery().create_user_search_settings(
        session, user_settings
    )
    return user_settings_db
