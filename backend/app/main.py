from fastapi import FastAPI

from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper
from backend.app.routers import users

app = FastAPI()
app.include_router(users.router)

app.add_middleware(DBSessionMiddleware, db_url="postgresql://postgres:postgres@database:5432/postgres")

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}