import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

from database import Base
from app.main import app
from dependecies import get_db

from queries.user_query import UserQuery
from schemas.user_schema import UserObject

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@database:5432/test"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)

    yield db

    db.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def users(db):
    UserQuery().create_user(db, UserObject(username="abc",email="abc@gmail",hashed_password="pass"))
    UserQuery().create_user(db, UserObject(username="abc2",email="abc@gmail2",hashed_password="pass2"))