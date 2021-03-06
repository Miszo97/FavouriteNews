from database import Base
from enums import Category, Country, Language, Source
from sqlalchemy import Column, Enum, Integer
from sqlalchemy.schema import ForeignKey


class UserSearchSettings(Base):
    __tablename__ = "user_search_settings"
    id = Column(Integer(), primary_key=True)

    country = Column("country", Enum(Country))
    category = Column("category", Enum(Category))
    source = Column("source", Enum(Source))
    language = Column("language", Enum(Language))
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
