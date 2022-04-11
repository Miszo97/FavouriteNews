from enums import Category, Country, Language, Source
from models.user_search_settings import UserSearchSettings
from sqlalchemy.orm import Session


class UserSearchSettingsQuery:
    def create_user_search_settings(
        self, db: Session, new_settings: UserSearchSettings
    ) -> UserSearchSettings:
        db.add(new_settings)
        db.commit()
        db.refresh(new_settings)
        return new_settings

    def get_users_settings(self, db: Session) -> UserSearchSettings:
        users_settings = db.query(UserSearchSettings).all()
        return users_settings

    def get_user_search_settings_by_user_id(
        self, db: Session, user_id: int
    ) -> UserSearchSettings:
        user_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.user_id == user_id)
            .first()
        )
        return user_settings

    def set_category(
        self, db: Session, settings_id: int, category: Category
    ) -> UserSearchSettings:
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        user_search_settings.category = category
        db.commit()
        return user_search_settings

    def set_country(
        self, db: Session, settings_id: int, country: Country
    ) -> UserSearchSettings:
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        user_search_settings.country = country
        db.commit()
        return user_search_settings

    def set_language(
        self, db: Session, settings_id: int, language: Language
    ) -> UserSearchSettings:
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        user_search_settings.language = language
        db.commit()
        return user_search_settings

    def set_source(
        self, db: Session, settings_id: int, source: Source
    ) -> UserSearchSettings:
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        user_search_settings.source = source
        db.commit()
        return user_search_settings


    def delete_user_search_settings(
        self, db: Session, settings_id: int
    ) -> UserSearchSettings:
        user_search_settings = (
            db.query(UserSearchSettings)
            .filter(UserSearchSettings.id == settings_id)
            .first()
        )
        db.delete(user_search_settings)
        db.commit()
        return user_search_settings

    def update_user_search_settings(self, db: Session, user_id, update_data):

        db.query(UserSearchSettings).filter(
            UserSearchSettings.user_id == user_id
        ).update(update_data)
        db.commit()

        user_settings = self.get_user_search_settings_by_user_id(db, user_id)

        return user_settings

