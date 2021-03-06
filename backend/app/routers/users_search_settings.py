from dependencies.current_user import get_current_user
from dependencies.database_session import get_db
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models.user_search_settings import UserSearchSettings
from queries.user_serach_settings_query import UserSearchSettingsQuery
from schemas.user_schema import UserObject
from schemas.user_search_settings_schema import (
    UserSearchSettingsInput,
    UserSearchSettingsObject,
)

router = APIRouter()

user_search_settings_query = UserSearchSettingsQuery()


@router.get("/users/me/user-search-settings", response_model=UserSearchSettingsObject)
async def get_user_search_settings(
    db=Depends(get_db), current_user: UserObject = Depends(get_current_user)
):
    user_settings = UserSearchSettingsQuery().get_user_search_settings_by_user_id(
        db, current_user.id
    )
    return user_settings


@router.post("/users/me/user-search-settings", response_model=UserSearchSettingsObject)
async def create_user_search_settings(
    user_settings: UserSearchSettingsInput,
    current_user: UserObject = Depends(get_current_user),
    db=Depends(get_db),
):
    user_settings_db = UserSearchSettingsQuery().create_user_search_settings(
        db, UserSearchSettings(**user_settings.dict(), user_id=current_user.id)
    )
    return user_settings_db


@router.delete(
    "/users/{user_id}/user-search-settings", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user_search_settings(
    user_id: int,
    current_user: UserObject = Depends(get_current_user),
    db=Depends(get_db),
):

    if (
        user_search_settings_query.get_user_search_settings_by_user_id(db, user_id)
        is None
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "User search settings not found"},
        )

    user_search_settings_query.delete_user_search_settings(db, user_id)


@router.patch("/users/me/user-search-settings", response_model=UserSearchSettingsObject)
async def update_user_search_settings(
    new_settings_input_object: UserSearchSettingsInput,
    current_user: UserObject = Depends(get_current_user),
    db=Depends(get_db),
):

    update_data = new_settings_input_object.dict(exclude_unset=True)

    updated_settings = UserSearchSettingsQuery().update_user_search_settings(
        db, current_user.id, update_data
    )
    return updated_settings
