"""User model

Defines the SQLAlchemy ORM model for application users. The model is
used across authentication, repository and service layers.

Fields:
 - id: primary key integer, auto-increment
 - username: unique username used for login
 - email: unique email address for the user
 - password_hash: hashed password stored securely
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """Represents a user account in the database.

    Keep this model focused only on fields required for authentication and
    identification. Additional profile details should live in a separate
    table if needed.
    """

    __tablename__ = 'users'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Username used for authentication; must be unique
    username = Column(String(50), unique=True, nullable=False)

    # Contact / identification email; must be unique
    email = Column(String(100), unique=True, nullable=False)

    # Hashed password (never store plaintext passwords)
    password_hash = Column(String(128), nullable=False)

    def __repr__(self):
        """Developer-friendly representation (redacts password)."""
        return f"<User(username='{self.username}', email='{self.email}')>"