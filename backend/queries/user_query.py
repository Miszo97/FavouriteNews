from models.user import User
from database import SessionLocal

db = SessionLocal()

class UserQuery():
    def getUserById(user_id):
        user = db.query(User).filter(User.id==user_id).first()
        return user
    
    def setEmail(user_id, email):
        user = db.query(User).filter(User.id == user_id).first()
        user.email = email
        db.commit()
        return user

    def setUsername(user_id, username):
        user = db.query(User).filter(User.id == user_id).first()
        user.username = username
        db.commit()
        return user
