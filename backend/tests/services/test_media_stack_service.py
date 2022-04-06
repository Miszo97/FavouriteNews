import pytest
from enums import Category, Country, Language, Source
from services.media_stack_service import MediaStackService
from settings import MEDIA_STACK_API

media_stack_service = MediaStackService(api_key=MEDIA_STACK_API)


@pytest.mark.vcr()
def test_get_articles_by_parameters():
    articles = media_stack_service.get_news_by_parameters(
        country=Country.US,
        language=Language.EN,
        category=Category.GENERAL,
        source=Source.CNN,
    )
    assert len(articles) == 25

    first_article = articles[0].dict()

    assert Country.US.value in first_article.values()
    assert Language.EN.value in first_article.values()
    assert Category.GENERAL.value in first_article.values()


@pytest.mark.vcr()
def test_get_articles_limit():
    articles = media_stack_service.get_news_by_parameters(
        country=Country.US,
        language=Language.EN,
        category=Category.GENERAL,
        source=Source.CNN,
        limit=5,
    )

    assert len(articles) == 5
