from typing import List, Optional

import requests
from enums import Category, Country, Language, Source
from services.schemas import Article
from settings import MEDIA_STACK_API


class MediaStackService:
    def __init__(self, api_key):
        self.api_key = api_key
        self._news_endpoint = "http://api.mediastack.com/v1/news"

    def get_news_by_parameters(
        self,
        country: Optional[Country] = None,
        language: Optional[Language] = None,
        category: Optional[Category] = None,
        source: Optional[Source] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> List[Article]:
        url = f"{self._news_endpoint}" "?" f"access_key={MEDIA_STACK_API}"
        if country:
            url += f"&countries={country.value}"

        if language:
            url += f"&languages={language.value}"

        if category:
            url += f"&categories={category.value}"

        if source:
            url += f"&sources={source.value}"

        if limit:
            url += f"&limit={limit}"

        if offset:
            url += f"&limit={offset}"

        response = requests.get(url)
        article_list = response.json()["data"]
        articles = [Article(**article) for article in article_list]

        return articles
