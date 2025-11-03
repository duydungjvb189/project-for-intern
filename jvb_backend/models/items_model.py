"""Item model

Defines the SQLAlchemy ORM model for items stored in the application.
This module contains the Item class which maps to the 'items' table.

Fields:
 - id: primary key integer, auto-increment
 - name: text name for the item (required)
"""

from sqlalchemy import String, Integer, Column
from models.user_model import Base


class Item(Base):
    """Represents an item record in the database.

    This is a lightweight model used by the repository and service layers.
    """

    __tablename__ = 'items'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Human-readable name for the item. Required field.
    name = Column(String(100), nullable=False)

    def __repr__(self):
        """Return a concise developer-friendly representation."""
        return f"<Item(name='{self.name}')>"