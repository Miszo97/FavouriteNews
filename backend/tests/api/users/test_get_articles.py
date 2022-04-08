import pytest
from enums import Category, Country, Language, Source
from fastapi import status
from tests.conftest import create_user, create_user_serach_settings

endpoint = "/users/me/followed-articles"


def test_get_articles_unauthorized(client, session):
    create_user(session)
    payload = {"limit": "10", "offset": "0"}

    response = client.post(endpoint, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.vcr(record_mode="new_episodes")
def test_get_articles(authorized_client, session):
    create_user_serach_settings(
        session,
        user_id=authorized_client.user.id,
        country=Country.US,
        language=Language.EN,
        category=Category.GENERAL,
        source=Source.CNN,
    )

    payload = {"limit": "10", "offset": "0"}

    response = authorized_client.post(endpoint, data=payload)

    articles = response.json()

    assert len(articles) == 10

    assert sum([1 for article in articles if article["country"] == Country.US.value]) == 10
    assert sum([1 for article in articles if article["language"] == Language.EN.value]) == 10
    assert sum([1 for article in articles if article["category"] == Category.GENERAL.value])== 10
