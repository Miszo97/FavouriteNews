from dependencies.current_user import get_current_user
from fastapi import APIRouter, Depends
from schemas.user_schema import UserObject

router = APIRouter()


@router.get("/users/me/", response_model=UserObject)
async def read_users_me(current_user: UserObject = Depends(get_current_user)):
    return current_user
