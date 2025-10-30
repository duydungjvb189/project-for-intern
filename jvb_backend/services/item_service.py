from fastapi import HTTPException
from repositories.item_repository import ItemRepository
from schemas.item_schemas import ItemCreate, ItemUpdate

def create_item_service(db, item_data: ItemCreate):
    repo = ItemRepository(db)
    new_item = repo.create(item_data.name)

    return {
        "detail": "Item created successfully",
        "item": new_item
    }

def get_item_by_id_service(db, item_id: int):
    repo = ItemRepository(db)
    item = repo.get_by_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def get_all_items_service(db):
    repo = ItemRepository(db)
    items = repo.get_all()

    return items

def update_item_service(db, item_id: int, item_data: ItemUpdate):
    repo = ItemRepository(db)
    item = repo.get_by_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    repo.update(item_id, item_data.name)

    return {
        "detail": "Item updated successfully",
        "item": item
    }

def delete_item_service(db, item_id: int):
    repo = ItemRepository(db)
    item = repo.get_by_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
   
    repo.delete(item_id)
    
    return {"detail": "Item deleted successfully"}