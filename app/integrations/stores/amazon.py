"""
Amazon Mexico Integration.

Amazon tiene API oficial (Product Advertising API) que requiere registro.
Documentación: https://webservices.amazon.com/paapi5/documentation/
"""
from typing import List, Optional, Dict, Any
from ..api_adapter import APIAdapter
from ..base import Product
import hashlib
import hmac
import datetime
from urllib.parse import quote


class AmazonMXIntegration(APIAdapter):
    """
    Integration with Amazon Mexico using Product Advertising API.

    Requiere credenciales:
    - Access Key
    - Secret Key
    - Partner Tag (Associate ID)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Amazon MX integration.

        Args:
            config: Configuration dictionary
                Required keys:
                - access_key: AWS Access Key
                - secret_key: AWS Secret Key
                - partner_tag: Amazon Associate ID
        """
        super().__init__(
            store_name="Amazon MX",
            config=config or {},
            base_url="https://webservices.amazon.com.mx/paapi5",
            auth_type="none",  # Custom signing
            rate_limit=1  # 1 request per second (API limit)
        )

        self.access_key = self.config.get('access_key', '')
        self.secret_key = self.config.get('secret_key', '')
        self.partner_tag = self.config.get('partner_tag', '')
        self.marketplace = "www.amazon.com.mx"

    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        """
        Fetch products from Amazon PA-API.

        Args:
            query: Search keywords
            category: Category filter (Amazon BrowseNodeId)
            limit: Maximum products to return

        Returns:
            List of Product objects
        """
        if not all([self.access_key, self.secret_key, self.partner_tag]):
            print("⚠️  Amazon API credentials not configured")
            print("   Configure: access_key, secret_key, partner_tag")
            return []

        if not query:
            return []

        try:
            # Build PA-API SearchItems request
            payload = {
                "Keywords": query,
                "Resources": [
                    "Images.Primary.Large",
                    "ItemInfo.Title",
                    "Offers.Listings.Price"
                ],
                "ItemCount": min(limit, 10),  # PA-API max is 10 per request
                "PartnerTag": self.partner_tag,
                "PartnerType": "Associates",
                "Marketplace": self.marketplace
            }

            if category:
                payload["SearchIndex"] = category

            # Make signed request
            response = await self._make_paapi_request("/searchitems", payload)

            # Parse response
            products = self._parse_search_response(response)
            return self.validate_products(products)

        except Exception as e:
            print(f"Error fetching Amazon products: {e}")
            return []

    async def _make_paapi_request(
        self,
        endpoint: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make signed request to PA-API.

        PA-API requires AWS Signature Version 4.
        """
        # TODO: Implement AWS Signature V4
        # Por ahora retornamos estructura vacía
        return {"SearchResult": {"Items": []}}

    def _parse_search_response(self, response: Dict[str, Any]) -> List[Product]:
        """Parse Amazon PA-API search response."""
        products = []

        items = response.get("SearchResult", {}).get("Items", [])

        for item in items:
            try:
                product = self._parse_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"Error parsing Amazon item: {e}")
                continue

        return products

    def _parse_item(self, item: Dict[str, Any]) -> Optional[Product]:
        """Parse a single Amazon item."""
        try:
            # Extract data
            asin = item.get("ASIN")
            title = item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue")

            # Price
            offers = item.get("Offers", {}).get("Listings", [])
            price = None
            if offers:
                price_info = offers[0].get("Price", {})
                price = price_info.get("Amount")

            # Image
            images = item.get("Images", {}).get("Primary", {})
            image_url = images.get("Large", {}).get("URL", "")

            # Detail page URL
            detail_url = item.get("DetailPageURL", "")

            if not all([asin, title, price, detail_url]):
                return None

            return Product(
                name=title,
                price=float(price),
                store_name=self.store_name,
                store_url=detail_url,
                image_url=image_url,
                sku=asin,
                currency="MXN"
            )

        except Exception as e:
            print(f"Error parsing Amazon item: {e}")
            return None

    async def test_connection(self) -> bool:
        """Test Amazon API connection."""
        if not all([self.access_key, self.secret_key, self.partner_tag]):
            return False

        try:
            # Try a simple search
            products = await self.fetch_products(query="test", limit=1)
            return True
        except Exception as e:
            print(f"Amazon connection test failed: {e}")
            return False


class AmazonFallbackIntegration:
    """
    Fallback: Si no tenemos credenciales de PA-API,
    podemos usar datos de ejemplo o preparar para scraping autorizado.
    """

    def __init__(self):
        print("⚠️  Amazon PA-API no configurado")
        print("   Para usar Amazon, configura:")
        print("   - AWS Access Key")
        print("   - AWS Secret Key")
        print("   - Amazon Associate Partner Tag")
        print("   Registro: https://affiliate-program.amazon.com.mx/")
