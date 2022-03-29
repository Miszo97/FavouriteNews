from enums import Category, Country, Language, Source
from models.user_search_settings import UserSearchSettings
from queries.user_serach_settings_query import UserSearchSettingsQuery
from tests.conftest import create_user, create_user_serach_settings


def test_create_user_search_settings(session, create_user_instance):

    new_settings = UserSearchSettings(
        country=Country.AR,
        category=Category.HEALTH,
        source=Source.BBC,
        language=Language.FR,
        user_id=1,
    )
    assert len(session.query(UserSearchSettings).all()) == 0

    UserSearchSettingsQuery().create_user_search_settings(session, new_settings)
    assert len(session.query(UserSearchSettings).all()) == 1


def test_set_user_search_setting_attribute(session, create_user_instance):
    new_settings = UserSearchSettings(
        country=Country.AR,
        category=Category.HEALTH,
        source=Source.BBC,
        language=Language.FR,
        user_id=1,
    )
    settings_db = UserSearchSettingsQuery().create_user_search_settings(
        session, new_settings
    )

    UserSearchSettingsQuery().set_category(session, settings_db.id, "BUSINESS")
    assert settings_db.category.value == "Business News"

    UserSearchSettingsQuery().set_country(session, settings_db.id, "BR")
    assert settings_db.country.value == "Brazil"

    UserSearchSettingsQuery().set_language(session, settings_db.id, "HE")
    assert settings_db.language.value == "Hebrew"

    UserSearchSettingsQuery().set_source(session, settings_db.id, "CNN")
    assert settings_db.source.value == "cnn"


def test_get_user_search_settings_by_user_id(
    session, create_user_instance, create_user_search_settings_instance
):
    user_search_settings = (
        UserSearchSettingsQuery().get_user_search_settings_by_user_id(
            session, user_id=1
        )
    )

    assert user_search_settings.country.value == "Poland"


def test_get_users_settings(session):
    create_user(session)
    create_user(session, username="Jon", email="John@gmail.com", id=2)
    create_user(session, username="Paul", email="Paul@gmail.com", id=3)

    create_user_serach_settings(session)
    create_user_serach_settings(session, user_id=2, id=2)
    create_user_serach_settings(session, user_id=3, id=3)

    users_search_settings = UserSearchSettingsQuery().get_users_settings(session)

    assert len(users_search_settings) == 3
