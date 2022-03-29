from enums import Category, Country, Language, Source
from models.user_search_settings import UserSearchSettings
from schemas.user_search_settings_schema import UserSearchSettingsObject
from sqlalchemy.orm import Session


class UserSearchSettingsQuery:
    def create_user_search_settings(
        self, db: Session, settings: UserSearchSettingsObject
    ):
        new_settings = UserSearchSettings(
            id=settings.id,
            country=settings.country,
            category=settings.category,
            source=settings.source,
            language=settings.language,
            user_id=settings.user_id,
        )
        db.add(new_settings)
        db.commit()
        db.refresh(new_settings)
        return new_settings

    def get_users_settings(self, db: Session):
        users_settings = db.query(UserSearchSettings).all()
        return users_settings

    def get_user_search_settings_by_user_id(self, db: Session, user_id: int):
        user_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.user_id == user_id)
            .first()
        )
        return user_settings

    def set_category(self, db: Session, settings_id: int, category: Category):
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        user_search_settings.category = category
        db.commit()
        return user_search_settings

    def set_country(self, db: Session, settings_id: int, country: Country):
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        user_search_settings.country = country
        db.commit()
        return user_search_settings

    def set_language(self, db: Session, settings_id: int, language: Language):
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        user_search_settings.language = language
        db.commit()
        return user_search_settings

    def set_source(self, db: Session, settings_id: int, source: Source):
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        user_search_settings.source = source
        db.commit()
        return user_search_settings
