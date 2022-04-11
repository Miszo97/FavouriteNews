from typing import Optional

from pydantic import BaseModel


class UserObject(BaseModel):
    id: Optional[int]
    username: str
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UserInput(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]


class UserInDB(UserObject):
    hashed_password: str
