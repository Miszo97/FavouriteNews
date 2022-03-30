import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.environ.get("ALGORITHM")
DATABASE_LOGIN = os.environ.get("DATABASE_LOGIN")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
