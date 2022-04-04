from dependencies.current_user import get_current_user
from dependencies.database_session import get_db
from fastapi import APIRouter, Depends
from models.user_search_settings import UserSearchSettings
from queries.user_serach_settings_query import UserSearchSettingsQuery
from schemas.user_schema import UserObject
from schemas.user_search_settings_schema import UserSearchSettingsObject

router = APIRouter()


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
    user_settings: UserSearchSettingsObject,
    current_user: UserObject = Depends(get_current_user),
    db=Depends(get_db),
):

    new_user_settings = UserSearchSettings(
        country=user_settings.country,
        category=user_settings.category,
        source=user_settings.source,
        language=user_settings.language,
        user_id=current_user.id,
    )
    user_settings_db = UserSearchSettingsQuery().create_user_search_settings(
        db, new_user_settings
    )
    return user_settings_db


@router.patch("/users/me/user-search-settings", response_model=UserSearchSettingsObject)
async def update_user_search_settings(
    new_settings: UserSearchSettingsObject,
    current_user: UserObject = Depends(get_current_user),
    db=Depends(get_db),
):

    stored_settings_data = (
        UserSearchSettingsQuery().get_user_search_settings_by_user_id(
            db, current_user.id
        )
    )

    stored_settings_model = UserSearchSettingsObject.from_orm(stored_settings_data)

    update_data = new_settings.dict(exclude_unset=True)

    updated_settings = stored_settings_model.copy(update=update_data)

    return updated_settings