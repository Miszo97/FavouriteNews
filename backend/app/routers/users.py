from typing import List, Optional

from dependencies.current_user import get_current_user
from dependencies.database_session import get_db
from fastapi import APIRouter, Depends, Form
from models import User
from queries.user_query import UserQuery
from schemas.user_schema import UserObject
from sqlalchemy.orm import Session
from utils.authentication import get_password_hash

router = APIRouter()


@router.post("/users", response_model=UserObject, status_code=201)
async def register(
    username: str = Form(...),
    password: str = Form(...),
    email: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    new_user = User(username=username, email=email)
    new_user.hashed_password = get_password_hash(password)
    return UserQuery().create_user(db, new_user)


@router.get(
    "/users", response_model=List[UserObject], dependencies=[Depends(get_current_user)]
)
async def get_users(db=Depends(get_db)):
    users = UserQuery().get_users(db)
    return users


@router.get("/users/me", response_model=UserObject)
async def get_user(current_user: UserObject = Depends(get_current_user)):
    user = current_user
    return user


@router.patch("/users/me", response_model=UserObject)
async def update_user(
    new_user: UserObject,
    current_user: UserObject = Depends(get_current_user),
    db=Depends(get_db),
):
    stored_user_model = UserObject.from_orm(current_user)

    update_data = new_user.dict(exclude_unset=True)

    updated_user = stored_user_model.copy(update=update_data)

    return updated_user
