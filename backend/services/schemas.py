from datetime import datetime
from typing import Optional

from enums import Category, Country, Language
from pydantic import BaseModel, HttpUrl


class Article(BaseModel):
    author: Optional[str]
    title: str
    description: str
    url: HttpUrl
    source: str
    image: Optional[HttpUrl]
    category: Category
    language: Language
    country: Country
    published_at: datetime
