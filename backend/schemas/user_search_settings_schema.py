from pydantic import BaseModel
from typing import Optional

class UserSearchSettingsObject(BaseModel):
    id: Optional[int]
    user_id: int

    class Config:
        orm_mode = True
