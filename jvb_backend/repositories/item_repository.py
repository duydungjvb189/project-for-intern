from sqlalchemy.orm import Session
from models.items_model import Item

class ItemRepository:
    # Initialize the repository with a SQLAlchemy Session.
    def __init__(self, db: Session):
        self.db = db

    # Create a new item and save it to the database.
    def create(self, name: str):
        new_item = Item(name=name)
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    # Retrieve an item by its ID.
    def get_by_id(self, item_id: int):
        return self.db.query(Item).filter(Item.id == item_id).first()

    # Retrieve all items from the database.
    def get_all(self):
        return self.db.query(Item).all()

    # Update the name of an existing item.
    def update(self, item_id: int, name: str):
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            item.name = name
            self.db.commit()
            self.db.refresh(item)
        return item

    # Delete an item by its ID.
    def delete(self, item_id: int):
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            self.db.delete(item)
            self.db.commit()
        return item