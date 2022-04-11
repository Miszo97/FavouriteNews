from models.user import User
from sqlalchemy.orm import Session


class UserQuery:
    def create_user(self, db: Session, new_user: User) -> User:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_users(self, db: Session) -> User:
        users = db.query(User).all()
        return users

    def get_user_by_id(self, db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        return user

    def get_user_by_username(self, db: Session, username: str) -> User:
        user = db.query(User).filter(User.username == username).first()
        return user

    def set_email(self, db: Session, user_id: int, email: str) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        user.email = email
        db.commit()
        return user

    def set_username(self, db: Session, user_id: int, username: str) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        user.username = username
        db.commit()
        return user

    def update_user(self, db: Session, user_id, update_data) -> User:

        db.query(User).filter(User.id == user_id).update(update_data)
        db.commit()

        user = db.query(User).filter(User.id == user_id).first()

        return user
