from backend.database import Base
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    username = Column(String(25),nullable=False,unique=True)
    email = Column(String(25),nullable=True,unique=True)
    # user_settings = relationship("UserSearchSettings")