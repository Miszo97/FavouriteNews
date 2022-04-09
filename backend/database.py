from settings import DATABASE_HOST, POSTGRES_LOGIN, POSTGRES_PASSWORD
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:5432/postgres"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
