from typing import Optional

from pydantic import BaseModel


class UserObject(BaseModel):
    id: Optional[int]
    username: str
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UserInDB(UserObject):
    hashed_password: str
