"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Store(Base):
    """Store model - represents online stores."""
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # "Amazon MX", "Walmart MX"
    url = Column(String, nullable=False)  # Base URL
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    products = relationship("Product", back_populates="store")

    def __repr__(self):
        return f"<Store(name='{self.name}')>"


class Product(Base):
    """Product model - represents products from stores."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    store_url = Column(String, nullable=False)  # URL del producto específico
    sku = Column(String, index=True)  # SKU/ID del producto en la tienda
    price = Column(Float, nullable=False)
    currency = Column(String, default="MXN")
    image_url = Column(String)
    available = Column(Integer, default=1)  # 1 = disponible, 0 = no disponible
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    store = relationship("Store", back_populates="products")

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"
