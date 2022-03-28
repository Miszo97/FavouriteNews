from app.routers import users
from fastapi import FastAPI

app = FastAPI()
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
