from models.user import User
from database import SessionLocal

class UserQuery():
    def get_user_by_id(user_id):
        user = SessionLocal().query(User).filter(User.id==user_id).first()
        return user
    
    def get_user_by_username(username):
        user = SessionLocal().query(User).filter(User.username==username).first()
        return user
    
    def set_email(user_id, email):
        user = SessionLocal().query(User).filter(User.id == user_id).first()
        user.email = email
        with SessionLocal() as session:
            session.commit()
        return user

    def set_username(user_id, username):
        user = SessionLocal().query(User).filter(User.id == user_id).first()
        user.username = username
        with SessionLocal() as session:
            session.commit()
        return user
