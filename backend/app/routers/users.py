from typing import List, Optional

from dependencies.current_user import get_current_user
from dependencies.database_session import get_db
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import JSONResponse
from models import User
from queries.user_query import UserQuery
from queries.user_serach_settings_query import UserSearchSettingsQuery
from schemas.user_schema import UserInput, UserObject
from services.media_stack_service import MediaStackService
from services.schemas import Article
from settings import MEDIA_STACK_API_KEY
from sqlalchemy.orm import Session
from utils.authentication import get_password_hash

router = APIRouter()


@router.post("/users", response_model=UserObject, status_code=201)
async def register(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):

    user = UserQuery().get_user_by_email_or_username(db, email, username)
    if user:
        if user.username == username:
            detail = {"error": "username already exists"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=detail)
        if user.email == email:
            detail = {"error": "email already taken"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=detail)

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
    new_user_object: UserInput,
    current_user: UserObject = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = UserQuery().get_user_by_email_or_username(
        db, new_user_object.email, new_user_object.username
    )

    if user:
        if user.username is not None and user.username == new_user_object.username:
            detail = {"error": "username already exists"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=detail)

        if user.email is not None and user.email == new_user_object.email:
            detail = {"error": "email already taken"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=detail)

    update_data = new_user_object.dict(exclude_unset=True)
    updated_user = UserQuery().update_user(db, current_user.id, update_data)

    return updated_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: UserObject = Depends(get_current_user),
    db=Depends(get_db),
):
    user = UserQuery().get_user_by_id(db, user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    if user.id == current_user.id:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "You can not delete yourself"},
        )
    UserQuery().delete_user(db, user_id)
    return user


@router.get("/users/me/followed-articles", response_model=List[Article])
async def followed_articles(
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: Optional[int] = Form(None),
    offset: Optional[int] = Form(None),
):
    user = current_user
    user_settings = UserSearchSettingsQuery().get_user_search_settings_by_user_id(
        db, user.id
    )
    articles = MediaStackService(MEDIA_STACK_API_KEY).get_news_by_parameters(
        user_settings.country,
        user_settings.language,
        user_settings.category,
        user_settings.source,
        limit,
        offset,
    )
    return articles
