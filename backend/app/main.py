from app.routers import login, users
from fastapi import FastAPI

app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
