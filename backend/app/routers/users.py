from typing import Optional

from dependencies.current_user import get_current_user
from dependencies.database_session import get_db
from fastapi import APIRouter, Depends, Form
from models import User
from queries.user_query import UserQuery
from schemas.user_schema import UserObject
from sqlalchemy.orm import Session
from utils.authentication import pwd_context

router = APIRouter()


@router.get("/users/me", response_model=UserObject)
async def read_users_me(current_user: UserObject = Depends(get_current_user)):
    return current_user


@router.post("/users", response_model=UserObject, status_code=201)
async def register(
    username: str = Form(...),
    password: str = Form(...),
    email: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    new_user = User(username=username, email=email)
    new_user.hashed_password = pwd_context.hash(password)
    return UserQuery().create_user(db, new_user)
