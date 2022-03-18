from pydantic import BaseModel
from typing import Optional

class UserObject(BaseModel):
    id: Optional[int]
    username: str
    email: str
    hashed_password : str

    class Config:
        orm_mode = True