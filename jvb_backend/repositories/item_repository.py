from sqlalchemy.orm import Session
from models.items_model import Item

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str):
        new_item = Item(name=name)
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def get_by_id(self, item_id: int):
        return self.db.query(Item).filter(Item.id == item_id).first()

    def get_all(self):
        return self.db.query(Item).all()

    def update(self, item_id: int, name: str):
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            item.name = name
            self.db.commit()
            self.db.refresh(item)
        return item

    def delete(self, item_id: int):
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            self.db.delete(item)
            self.db.commit()
        return item