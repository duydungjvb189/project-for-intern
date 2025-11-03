from sqlalchemy.orm import Session
from models.user_model import User

class UserRepository:
    # Initialize the repository with a SQLAlchemy Session.
    def __init__(self, db: Session):
        self.db = db

    # Retrieve all users from the database.
    def get_all_users(self):
        return self.db.query(User).all()

    # Retrieve a user by their email address.
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    # Retrieve a user by their username.
    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    # Retrieve a user by their unique ID.
    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    # Create and persist a new user in the database.
    def create_user(self, username: str, password_hash: str, email: str):
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
