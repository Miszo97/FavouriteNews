import pytest
from enums import Category, Country, Language, Source
from fastapi import status
from tests.conftest import create_user_serach_settings

endpoint = "/users/me/followed-articles"


def test_get_articles_unauthorized(client, session):
    create_user_serach_settings(
        session,
        user_id=1,
        country=Country.US,
        language=Language.EN,
        category=Category.GENERAL,
        source=Source.CNN,
    )

    payload = {"limit": "10", "offset": "0"}

    response = client.get(endpoint, params=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.vcr(record_mode="new_episodes")
def test_get_articles(authorized_client, session):

    create_user_serach_settings(
        session,
        user_id=1,
        country=Country.US,
        language=Language.EN,
        category=Category.GENERAL,
        source=Source.CNN,
    )

    payload = {"limit": "10", "offset": "0"}

    response = authorized_client.get(endpoint, params=payload)

    articles = response.json()
    assert len(articles) == 10

    articles_string = response.text()

    assert articles_string.count(Country.US.value) == 10
    assert articles_string.count(Language.EN.value) == 10
    assert articles_string.count(Category.GENERAL.value) == 10
