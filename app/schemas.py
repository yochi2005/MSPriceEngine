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


class CategoryBase(BaseModel):
    """Base schema for Category."""
    name: str
    slug: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a Category."""
    pass


class Category(CategoryBase):
    """Schema for Category response."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base schema for Product."""
    name: str
    store_id: int
    category_id: Optional[int] = None
    store_url: str
    sku: Optional[str] = None
    price: float
    currency: str = "MXN"
    image_url: Optional[str] = None
    available: int = 1


class ProductCreate(ProductBase):
    """Schema for creating a Product."""
    pass


class ProductBulkCreate(BaseModel):
    """Schema for bulk creating products."""
    products: list[ProductCreate]


class Product(ProductBase):
    """Schema for Product response."""
    id: int
    last_updated: datetime
    created_at: datetime
    store: Store
    category: Optional[Category] = None

    class Config:
        from_attributes = True


class PaginationMeta(BaseModel):
    """Schema for pagination metadata."""
    page: int
    per_page: int
    total: int
    total_pages: int


class ProductSearchResponse(BaseModel):
    """Schema for search response."""
    products: list[Product]
    pagination: PaginationMeta


class BulkCreateResponse(BaseModel):
    """Schema for bulk create response."""
    created: int
    failed: int
    errors: list[str]
