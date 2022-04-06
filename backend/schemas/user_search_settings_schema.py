from typing import Optional

from enums import Category, Country, Language, Source
from pydantic import BaseModel


class UserSearchSettingsObject(BaseModel):
    id: Optional[int]
    country: Country
    category: Category
    source: Source
    language: Language
    user_id: int

    class Config:
        orm_mode = True


class UserSearchSettingsInput(BaseModel):
    id: Optional[int]
    country: Optional[Country]
    category: Optional[Category]
    source: Optional[Source]
    language: Optional[Language]

    class Config:
        orm_mode = True
