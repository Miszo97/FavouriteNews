from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Article(BaseModel):
    author: Optional[str]
    title: str
    description: str
    url: str
    source: str
    image: Optional[str]
    category: str
    language: str
    country: str
    published_at: datetime
