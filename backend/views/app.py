from fastapi import FastAPI

from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper
from fastapi_sqlalchemy import db 

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url="postgresql://postgres:postgres@database:5432/postgres")