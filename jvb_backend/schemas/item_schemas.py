"""Pydantic schemas for Item requests and responses.

This module defines the request/response shapes used by routers and
services for item-related operations. The schemas are intentionally
simple and focused on the fields used in the example app.
"""

from pydantic import BaseModel


class ItemCreate(BaseModel):
    """Schema used when creating a new item.

    Fields:
        name: Human-readable name of the item (required).
    """

    name: str


class ItemUpdate(BaseModel):
    """Schema used when updating an existing item.

    Currently only supports changing the `name` field; expand as needed.
    """

    name: str


class ItemResponse(BaseModel):
    """Schema returned in responses when sending item data to clients.

    Includes the database-assigned `id` plus the `name` field.
    """

    id: int
    name: str

    class Config:
        # Allows Pydantic to populate this model from ORM objects (SQLAlchemy)
        # when using e.g. `ItemResponse.model_validate(item)` or Pydantic v1's
        # `orm_mode`. In Pydantic v2 this is expressed via `from_attributes`.
        from_attributes = True