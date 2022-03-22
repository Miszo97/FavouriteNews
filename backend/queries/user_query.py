from models.user import User
from sqlalchemy.orm import Session

class UserQuery():
    def get_user_by_id(user_id):
        user = db.session.query(User).filter(User.id==user_id).first()
        return user
    
    def get_user_by_username(username):
        user = db.session.query(User).filter(User.username==username).first()
        return user
    
    def set_email(user_id, email):
        user = db.session.query(User).filter(User.id == user_id).first()
        user.email = email
        db.session.commit()
        return user

    def set_username(user_id, username):
        user = db.session.query(User).filter(User.id == user_id).first()
        user.username = username
        db.session.commit()
        return user
