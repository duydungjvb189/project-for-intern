"""Item service layer

Contains higher-level operations around items that orchestrate the
repository and provide application-friendly return values and errors.
Each function raises HTTPException when the requested resource doesn't
exist or when an operation cannot be completed.
"""

from fastapi import HTTPException
from repositories.item_repository import ItemRepository
from schemas.item_schemas import ItemCreate, ItemUpdate


def create_item_service(db, item_data: ItemCreate):
    """Create and persist a new item.

    Args:
        db: SQLAlchemy Session used for persistence.
        item_data: ItemCreate schema with the `name` field.

    Returns:
        A dict containing a success message and the created Item object.
    """
    repo = ItemRepository(db)
    new_item = repo.create(item_data.name)

    return {
        "detail": "Item created successfully",
        "item": new_item,
    }


def get_item_by_id_service(db, item_id: int):
    """Retrieve a single item by id.

    Args:
        db: SQLAlchemy Session.
        item_id: Primary key of the item to retrieve.

    Returns:
        The Item instance when found.

    Raises:
        HTTPException: 404 if the item does not exist.
    """
    repo = ItemRepository(db)
    item = repo.get_by_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def get_all_items_service(db):
    """Return all items from the database.

    Args:
        db: SQLAlchemy Session.

    Returns:
        A list of Item instances.
    """
    repo = ItemRepository(db)
    items = repo.get_all()

    return items


def update_item_service(db, item_id: int, item_data: ItemUpdate):
    """Update an existing item's name.

    Args:
        db: SQLAlchemy Session.
        item_id: Primary key of the item to update.
        item_data: ItemUpdate schema with the new `name`.

    Returns:
        A dict with a success message and the updated Item instance.

    Raises:
        HTTPException: 404 if the item does not exist.
    """
    repo = ItemRepository(db)
    item = repo.get_by_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    repo.update(item_id, item_data.name)

    return {
        "detail": "Item updated successfully",
        "item": item,
    }


def delete_item_service(db, item_id: int):
    """Delete an item by id.

    Args:
        db: SQLAlchemy Session.
        item_id: Primary key of the item to delete.

    Returns:
        A dict with a success message.

    Raises:
        HTTPException: 404 if the item does not exist.
    """
    repo = ItemRepository(db)
    item = repo.get_by_id(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    repo.delete(item_id)

    return {"detail": "Item deleted successfully"}