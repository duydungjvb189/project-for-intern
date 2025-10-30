from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from database import get_db
from services.item_service import (
    create_item_service,
    get_item_by_id_service,
    get_all_items_service,
    update_item_service,
    delete_item_service
)
from schemas.item_schemas import ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", status_code=201)
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    return create_item_service(db, item_data)

@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_by_id_service(db, item_id)

@router.get("/")
def get_all_items(db: Session = Depends(get_db)):
    return get_all_items_service(db)

@router.put("/{item_id}")
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    return update_item_service(db, item_id, item_data)

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return delete_item_service(db, item_id)