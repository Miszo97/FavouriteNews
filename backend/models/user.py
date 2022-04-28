from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(Integer(), primary_key=True)
    username = Column(String(25), nullable=False, unique=True)
    email = Column(String(25), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    user_settings = relationship("UserSearchSettings")
