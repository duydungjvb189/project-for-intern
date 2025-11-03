"""Item repository

Provides a thin repository layer around SQLAlchemy operations for the
Item model. This class encapsulates common CRUD operations so the service
layer doesn't need to deal with raw queries or session management.

Design notes:
 - Methods return the affected Item instance (or None) to let callers
   decide how to respond (e.g. raise 404, ignore, etc.).
 - The repository commits transactions immediately; if you need multi-step
   transactions, consider passing an external session/transaction scope.
"""

from sqlalchemy.orm import Session
from models.items_model import Item


class ItemRepository:
    """Repository for Item persistence operations.

    Args:
        db: SQLAlchemy Session instance used for DB operations.
    """

    def __init__(self, db: Session):
        # Store the session; caller is responsible for session lifecycle
        self.db = db

    def create(self, name: str) -> Item:
        """Create and persist a new Item.

        Args:
            name: The human readable name for the item.

        Returns:
            The newly created Item instance (with id populated).
        """
        new_item = Item(name=name)
        self.db.add(new_item)
        self.db.commit()
        # Refresh to load generated fields (e.g. id)
        self.db.refresh(new_item)
        return new_item

    def get_by_id(self, item_id: int) -> Item | None:
        """Retrieve an Item by its primary key.

        Returns None if no matching item is found.
        """
        return self.db.query(Item).filter(Item.id == item_id).first()

    def get_all(self) -> list[Item]:
        """Return a list of all Item records."""
        return self.db.query(Item).all()

    def update(self, item_id: int, name: str) -> Item | None:
        """Update the name of an existing item.

        If the item exists, commits the change and returns the updated
        instance. Returns None when the item does not exist.
        """
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            item.name = name
            self.db.commit()
            self.db.refresh(item)
        return item

    def delete(self, item_id: int) -> Item | None:
        """Delete an Item by id.

        Returns the deleted Item instance (detached) or None if not found.
        """
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            self.db.delete(item)
            self.db.commit()
        return item