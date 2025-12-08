"""
Liverpool Integration.

Liverpool podría proporcionar feeds XML/JSON o API para partners.
"""
from typing import List, Optional, Dict, Any
from ..api_adapter import APIAdapter
from ..base import Product, BaseIntegration
from ..parsers.json_parser import JSONFeedParser


class LiverpoolIntegration(BaseIntegration):
    """
    Integration with Liverpool using product feeds.

    Liverpool podría proporcionar feeds estructurados para partners.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Liverpool integration.

        Args:
            config: Configuration dictionary
                Optional keys:
                - feed_url: URL del feed (JSON/XML)
                - api_key: API key si se requiere
        """
        super().__init__(store_name="Liverpool", config=config or {})

        self.feed_url = self.config.get('feed_url', '')
        self.api_key = self.config.get('api_key', '')

        # Si tenemos feed_url, inicializar parser JSON
        if self.feed_url:
            self.parser = JSONFeedParser(store_name=self.store_name)

    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        """
        Fetch products from Liverpool.

        Args:
            query: Search keywords (filtering local)
            category: Category filter (filtering local)
            limit: Maximum products to return

        Returns:
            List of Product objects
        """
        if not self.feed_url:
            print("⚠️  Liverpool feed_url not configured")
            print("   Configure feed_url en config")
            return []

        try:
            # Fetch products from feed
            products = await self.parser.parse_from_url(self.feed_url)

            # Apply local filters
            if query:
                query_lower = query.lower()
                products = [
                    p for p in products
                    if query_lower in p.name.lower()
                ]

            if category:
                category_lower = category.lower()
                products = [
                    p for p in products
                    if p.category and category_lower in p.category.lower()
                ]

            # Validate and limit
            valid_products = self.validate_products(products)
            return valid_products[:limit]

        except Exception as e:
            print(f"Error fetching Liverpool products: {e}")
            return []

    async def test_connection(self) -> bool:
        """Test Liverpool connection."""
        if not self.feed_url:
            return False

        try:
            products = await self.fetch_products(limit=1)
            return len(products) > 0
        except Exception:
            return False


class LiverpoolAPIIntegration(APIAdapter):
    """
    Alternative integration if Liverpool provides an API.

    Esta clase está lista para cuando Liverpool proporcione API oficial.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Liverpool API integration.

        Args:
            config: Configuration with API credentials
        """
        super().__init__(
            store_name="Liverpool",
            config=config or {},
            base_url="https://www.liverpool.com.mx/api",  # Hypothetical
            auth_type="api_key",
            rate_limit=5
        )

        print("⚠️  Liverpool API integration (placeholder)")
        print("   API oficial no disponible públicamente")

    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        """Fetch products from Liverpool API."""
        # Placeholder
        print(f"⚠️  Liverpool API: Búsqueda '{query}' no implementada")
        print("   Esperando API oficial de Liverpool")
        return []

    async def test_connection(self) -> bool:
        """Test Liverpool API connection."""
        return False
