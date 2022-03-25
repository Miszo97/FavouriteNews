from models.user import User
from sqlalchemy.orm import Session
from schemas.user_schema import UserObject

class UserQuery():
    def create_user(self,db,user : UserObject):
        new_user = User(
            id = user.id,
            username = user.username,
            email = user.email,
            hashed_password = user.hashed_password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    def get_users(self,db):
        users = db.query(User).all()
        return users

    def get_user_by_id(self,db,user_id):
        user = db.session.query(User).filter(User.id==user_id).first()
        return user
    
    def get_user_by_username(self,db,username):
        user = db.session.query(User).filter(User.username==username).first()
        return user
    
    def set_email(self,db,user_id, email):
        user = db.session.query(User).filter(User.id == user_id).first()
        user.email = email
        db.session.commit()
        return user

    def set_username(self,db,user_id, username):
        user = db.session.query(User).filter(User.id == user_id).first()
        user.username = username
        db.session.commit()
        return user
