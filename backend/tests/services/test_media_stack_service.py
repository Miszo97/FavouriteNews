import pytest
from enums import Category, Country, Language, Source
from services.media_stack_service import MediaStackService
from settings import MEDIA_STACK_API

media_stack_service = MediaStackService(api_key=MEDIA_STACK_API)


@pytest.mark.vcr()
def test_get_artciles_by_parameters():
    articles = media_stack_service.get_news_by_parameters(
        country=Country.PL,
        language=Language.EN,
        category=Category.GENERAL,
        source=Source.CNN,
    )
    assert len(articles) == 25
