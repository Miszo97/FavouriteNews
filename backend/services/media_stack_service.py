from typing import List, Optional

import requests
from enums import Category, Country, Language, Source
from services.schemas import Article


class MediaStackService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_news_by_parameters(
        self,
        country: Optional[Country] = None,
        language: Optional[Language] = None,
        category: Optional[Category] = None,
        source: Optional[Source] = None,
    ) -> List[Article]:
        url = (
            "http://api.mediastack.com/v1/news?"
            "access_key=162b82c434e7ba8482f5b81b8d3d6334&"
            "languages=en&sources=cnn&category=sport&country=us "
        )

        response = requests.get(url)
        article_list = response.json()["data"]
        articles = [Article(**article) for article in article_list]
        return articles
