"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class StoreBase(BaseModel):
    """Base schema for Store."""
    name: str
    url: str


class StoreCreate(StoreBase):
    """Schema for creating a Store."""
    pass


class Store(StoreBase):
    """Schema for Store response."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base schema for Product."""
    name: str
    store_id: int
    store_url: str
    sku: Optional[str] = None
    price: float
    currency: str = "MXN"
    image_url: Optional[str] = None
    available: int = 1


class ProductCreate(ProductBase):
    """Schema for creating a Product."""
    pass


class Product(ProductBase):
    """Schema for Product response."""
    id: int
    last_updated: datetime
    created_at: datetime
    store: Store

    class Config:
        from_attributes = True


class ProductSearchResponse(BaseModel):
    """Schema for search response."""
    total: int
    products: list[Product]
