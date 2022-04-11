from typing import List, Optional

from dependencies.current_user import get_current_user
from dependencies.database_session import get_db
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import JSONResponse
from models import User
from queries.user_query import UserQuery
from queries.user_serach_settings_query import UserSearchSettingsQuery
from schemas.user_schema import UserObject
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
    email: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    if UserQuery().get_user_by_username(db, username):
        detail = {"error": "username already exists"}
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
    new_user: UserObject,
    current_user: UserObject = Depends(get_current_user),
):
    stored_user_model = UserObject.from_orm(current_user)

    update_data = new_user.dict(exclude_unset=True)

    updated_user = stored_user_model.copy(update=update_data)

    return updated_user


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
