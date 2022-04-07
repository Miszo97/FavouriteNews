from enums import Category, Country, Language, Source
from queries.user_serach_settings_query import UserSearchSettingsQuery
from tests.conftest import create_user_serach_settings


def test_get_user_search_settings(authorized_client, session):
    create_user_serach_settings(
        session, user_id=1, country=Country.PL, language=Language.EN
    )

    response = authorized_client.get("/users/me/user-search-settings")

    assert response.json().get("country") == Country.PL.value
    assert response.json().get("language") == Language.EN.value


def test_create_user_search_settings(authorized_client, session):
    data = {
        "country": Country.AT.value,
        "category": Category.TECHNOLOGY.value,
        "source": Source.BBC.value,
        "language": Language.PT.value,
    }

    response = authorized_client.post("/users/me/user-search-settings", json=data)
    user_search_settings_qs = UserSearchSettingsQuery().get_users_settings(session)

    assert len(user_search_settings_qs) == 1

    assert response.json().get("country") == Country.AT.value
    assert response.json().get("category") == Category.TECHNOLOGY.value
    assert response.json().get("source") == Source.BBC.value
    assert response.json().get("language") == Language.PT.value
    assert response.json().get("user_id") == 1


def test_update_user_search_settings(authorized_client, session):
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
    }
    response = authorized_client.patch("/users/me/user-search-settings", json=data)
    print(response.json())
    assert response.json().get("country") == Country.BR.value
    assert response.json().get("category") == Category.SPORTS.value
    assert response.json().get("source") == Source.BBC.value
    assert response.json().get("language") == Language.EN.value