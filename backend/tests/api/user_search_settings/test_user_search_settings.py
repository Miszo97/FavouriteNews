from enums import Category, Country, Language, Source
from queries.user_serach_settings_query import UserSearchSettingsQuery
from tests.conftest import create_user_serach_settings


def test_get_user_search_settings(authorized_client, session):
    create_user_serach_settings(
        session, user_id=1, country=Country.PL, language=Language.EN
    )

    authorization = {"Authorization": f"Bearer {authorized_client.token}"}
    response = authorized_client.get("/users/me/user-search-settings",
                                     headers=authorization)

    assert response.json().get("country") == "Poland"
    assert response.json().get("language") == "English"


def test_create_user_search_settings(authorized_client, session):
    authorization = {"Authorization": f"Bearer {authorized_client.token}"}

    data = {
        "country": Country.AT.value,
        "category": Category.TECHNOLOGY.value,
        "source": Source.BBC.value,
        "language": Language.PT.value,
    }

    response = authorized_client.post(
        "/users/me/user-search-settings", json=data, headers=authorization
    )
    user_search_settings_qs = UserSearchSettingsQuery().get_users_settings(session)

    assert len(user_search_settings_qs) == 1

    assert response.json().get("country") == "Austria"
    assert response.json().get("category") == "Technology News"
    assert response.json().get("source") == "bbc"
    assert response.json().get("language") == "Portuguese"
    assert response.json().get("user_id") == 1


def test_update_user_search_settings(authorized_client, session):
    authorization = {"Authorization": f"Bearer {authorized_client.token}"}

    create_user_serach_settings(
        session,
        user_id=1,
        country=Country.PL,
        language=Language.EN,
        source=Source.BBC,
        category=Category.GENERAL,
    )

    data = {
        "country": Country.BR.value,
        "category": Category.SPORTS.value,
        "source": Source.CNN.value,
        "language": Language.NO.value,
        "user_id": 1,
    }
    response = authorized_client.patch(
        "/users/me/user-search-settings", json=data, headers=authorization
    )

    assert response.json().get("country") == "Brazil"
    assert response.json().get("category") == "Sport News"
    assert response.json().get("source") == "cnn"
    assert response.json().get("language") == "Norwegian"
