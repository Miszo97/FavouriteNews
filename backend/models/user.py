from database import Base
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import relationship

from models.user_search_settings import UserSearchSettings

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    username = Column(String(25),nullable=False,unique=True)
    email = Column(String(25),nullable=True,unique=True)
    hashed_password = Column(String(200), nullable=False)
    user_settings = relationship("UserSearchSettings")