from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.items_model import Item
from schemas.item_schemas import ItemCreate, ItemUpdate

def create_item_service(db: Session, item_data: ItemCreate):
    new_item = Item(name=item_data.name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {
        "detail": "Item created successfully",
        "item": new_item
    }

def get_item_by_id_service(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def get_all_items_service(db: Session):
    items = db.query(Item).all()
    return items

def update_item_service(db: Session, item_id: int, item_data: ItemUpdate):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = item_data.name
    db.commit()
    db.refresh(item)
    return {
        "detail": "Item updated successfully",
        "item": item
    }

def delete_item_service(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Item deleted successfully"}