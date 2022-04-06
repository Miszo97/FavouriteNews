from app.routers import login, users, users_search_settings
from fastapi import FastAPI

app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)
app.include_router(users_search_settings.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
