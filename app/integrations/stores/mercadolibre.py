"""
Mercado Libre API Integration.

Official API: https://developers.mercadolibre.com.mx/
No authentication required for public search endpoints.
"""
from typing import List, Optional, Dict, Any
from ..api_adapter import PaginatedAPIAdapter
from ..base import Product


class MercadoLibreIntegration(PaginatedAPIAdapter):
    """
    Integration with Mercado Libre Mexico API.

    Uses the public search API to fetch products.
    Documentation: https://developers.mercadolibre.com.mx/en_us/items-and-searches
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Mercado Libre integration.

        Args:
            config: Optional configuration (not required for public API)
        """
        super().__init__(
            store_name="Mercado Libre",
            config=config or {},
            base_url="https://api.mercadolibre.com",
            auth_type="none",
            rate_limit=5  # Conservative rate limit
        )

        # Mercado Libre Mexico site ID
        self.site_id = "MLM"

    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        """
        Fetch products from Mercado Libre API.

        Args:
            query: Search query
            category: Category filter (Mercado Libre category ID)
            limit: Maximum number of products to return

        Returns:
            List of Product objects
        """
        if not query:
            return []

        # Build search params
        params = {
            'q': query,
            'limit': min(limit, 50),  # ML API max is 50 per page
        }

        if category:
            params['category'] = category

        try:
            # Fetch products (with pagination if needed)
            if limit > 50:
                # Need multiple pages
                max_pages = (limit + 49) // 50
                products = await self.fetch_all_pages(
                    endpoint=f"/sites/{self.site_id}/search",
                    params=params,
                    response_parser=self._parse_search_response,
                    max_pages=max_pages,
                    page_key="offset",
                    page_size_key="limit"
                )
            else:
                # Single request
                response = await self._make_request(
                    f"/sites/{self.site_id}/search",
                    params=params
                )
                products = self._parse_search_response(response)

            # Validate and return
            return self.validate_products(products[:limit])

        except Exception as e:
            print(f"Error fetching Mercado Libre products: {e}")
            return []

    def _parse_search_response(self, response: Dict[str, Any]) -> List[Product]:
        """
        Parse Mercado Libre search response.

        Args:
            response: API response dictionary

        Returns:
            List of Product objects
        """
        products = []

        results = response.get('results', [])

        for item in results:
            try:
                product = self._parse_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"Error parsing ML item: {e}")
                continue

        return products

    def _parse_item(self, item: Dict[str, Any]) -> Optional[Product]:
        """
        Parse a single Mercado Libre item.

        Args:
            item: Item dictionary from API

        Returns:
            Product object or None
        """
        try:
            # Required fields
            item_id = item.get('id')
            title = item.get('title')
            price = item.get('price')
            permalink = item.get('permalink')
            thumbnail = item.get('thumbnail')

            if not all([item_id, title, price, permalink]):
                return None

            # Get category name if available
            category_name = None
            if 'category_id' in item:
                category_name = item.get('category_id')

            # Get high-resolution image if available
            image_url = thumbnail
            if 'thumbnail' in item and thumbnail:
                # Convert thumbnail to full image URL
                # ML thumbnails can be upgraded to full size
                image_url = thumbnail.replace('-I.jpg', '-O.jpg')

            # Get currency (usually MXN for MLM)
            currency = item.get('currency_id', 'MXN')

            # Check availability
            available = item.get('available_quantity', 0) > 0

            return Product(
                name=title,
                price=float(price),
                store_name=self.store_name,
                store_url=permalink,
                image_url=image_url,
                category=category_name,
                sku=item_id,
                currency=currency,
                available=available
            )

        except Exception as e:
            print(f"Error parsing ML item: {e}")
            return None

    async def test_connection(self) -> bool:
        """
        Test Mercado Libre API connection.

        Returns:
            True if connection successful
        """
        try:
            # Simple test: fetch site info
            response = await self._make_request(f"/sites/{self.site_id}")
            return response.get('id') == self.site_id
        except Exception as e:
            print(f"Mercado Libre connection test failed: {e}")
            return False

    async def get_categories(self) -> List[Dict[str, str]]:
        """
        Get available categories from Mercado Libre.

        Returns:
            List of category dictionaries with 'id' and 'name'
        """
        try:
            response = await self._make_request(f"/sites/{self.site_id}/categories")
            return [
                {'id': cat['id'], 'name': cat['name']}
                for cat in response
            ]
        except Exception as e:
            print(f"Error fetching ML categories: {e}")
            return []
