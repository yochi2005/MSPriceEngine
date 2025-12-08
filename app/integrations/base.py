"""
Base classes for store integrations.

All store integrations (API, XML, CSV, JSON) must inherit from BaseIntegration.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    """
    Standardized product data structure.

    All integrations must return products in this format.
    """
    name: str
    price: float
    store_name: str
    store_url: str
    image_url: str
    category: Optional[str] = None
    sku: Optional[str] = None
    currency: str = "MXN"
    available: bool = True

    def validate(self) -> bool:
        """Validate that all required fields are present."""
        if not self.name or len(self.name.strip()) == 0:
            return False
        if not self.price or self.price <= 0:
            return False
        if not self.store_url or not self.store_url.startswith('http'):
            return False
        if not self.image_url or not self.image_url.startswith('http'):
            return False
        return True


class BaseIntegration(ABC):
    """
    Abstract base class for all store integrations.

    Each store integration (API, XML, CSV, JSON) must implement this interface.
    """

    def __init__(self, store_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the integration.

        Args:
            store_name: Name of the store (e.g., "Mercado Libre", "Coppel")
            config: Optional configuration dictionary (API keys, feed URLs, etc.)
        """
        self.store_name = store_name
        self.config = config or {}

    @abstractmethod
    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        """
        Fetch products from the store.

        Args:
            query: Optional search query
            category: Optional category filter
            limit: Maximum number of products to return

        Returns:
            List of Product objects
        """
        pass

    @abstractmethod
    async def test_connection(self) -> bool:
        """
        Test if the integration is working.

        Returns:
            True if connection successful, False otherwise
        """
        pass

    def validate_products(self, products: List[Product]) -> List[Product]:
        """
        Validate and filter products.

        Args:
            products: List of products to validate

        Returns:
            List of valid products only
        """
        return [p for p in products if p.validate()]
