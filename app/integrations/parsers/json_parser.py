"""
JSON Feed Parser for product catalogs.

Supports JSON feeds from stores like Coppel.
"""
import json
from typing import List, Optional, Dict, Any
from ..base import Product
import httpx


class JSONFeedParser:
    """
    Parse JSON product feeds.

    Supports various JSON structures:
    - Array of products: [{"name": "...", "price": ...}, ...]
    - Nested structure: {"products": [...], "data": [...]}
    - API responses with metadata
    """

    def __init__(self, store_name: str, product_path: Optional[str] = None):
        """
        Initialize JSON parser.

        Args:
            store_name: Name of the store providing the feed
            product_path: Optional path to products in nested JSON
                Examples: "products", "data.items", "results.products"
        """
        self.store_name = store_name
        self.product_path = product_path

    async def parse_from_url(self, url: str) -> List[Product]:
        """
        Fetch and parse JSON feed from URL.

        Args:
            url: URL of the JSON feed

        Returns:
            List of Product objects
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return self.parse_from_string(response.text)

    def parse_from_file(self, file_path: str) -> List[Product]:
        """
        Parse JSON feed from local file.

        Args:
            file_path: Path to JSON file

        Returns:
            List of Product objects
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return self.parse_from_string(f.read())

    def parse_from_string(self, json_string: str) -> List[Product]:
        """
        Parse JSON string into products.

        Args:
            json_string: JSON content as string

        Returns:
            List of Product objects
        """
        try:
            data = json.loads(json_string)
            return self.parse_from_dict(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return []

    def parse_from_dict(self, data: Any) -> List[Product]:
        """
        Parse JSON dictionary/list into products.

        Args:
            data: Parsed JSON data (dict or list)

        Returns:
            List of Product objects
        """
        products = []

        # Navigate to products array using product_path
        product_list = self._extract_product_list(data)

        if not product_list:
            return products

        # Parse each product
        for item in product_list:
            if isinstance(item, dict):
                product = self._parse_item(item)
                if product:
                    products.append(product)

        return products

    def _extract_product_list(self, data: Any) -> List[Dict]:
        """
        Extract product list from JSON data.

        Args:
            data: Parsed JSON data

        Returns:
            List of product dictionaries
        """
        # If data is already a list, return it
        if isinstance(data, list):
            return data

        # If product_path is specified, navigate to it
        if self.product_path and isinstance(data, dict):
            keys = self.product_path.split('.')
            current = data
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return []

            if isinstance(current, list):
                return current

        # Try common JSON structures
        if isinstance(data, dict):
            # Try common keys for product arrays
            for key in ['products', 'items', 'data', 'results', 'records']:
                if key in data:
                    value = data[key]
                    if isinstance(value, list):
                        return value
                    elif isinstance(value, dict) and 'items' in value:
                        # Handle nested structure like {"data": {"items": [...]}}
                        if isinstance(value['items'], list):
                            return value['items']

        return []

    def _parse_item(self, item: Dict[str, Any]) -> Optional[Product]:
        """
        Parse a single JSON item into a Product.

        Args:
            item: Product dictionary from JSON

        Returns:
            Product object or None
        """
        try:
            # Extract fields using flexible key names
            name = self._get_field(item, ['name', 'title', 'product_name', 'productName'])
            price_value = self._get_field(item, ['price', 'cost', 'amount', 'precio'])
            url = self._get_field(item, ['url', 'link', 'product_url', 'productUrl'])
            image = self._get_field(item, ['image', 'image_url', 'imageUrl', 'thumbnail'])
            category = self._get_field(item, ['category', 'product_type', 'productType'])
            sku = self._get_field(item, ['sku', 'id', 'product_id', 'productId'])

            # Validate required fields
            if not name or not price_value or not url:
                return None

            # Parse price (handle different formats)
            price = self._parse_price(price_value)
            if price is None or price <= 0:
                return None

            return Product(
                name=name,
                price=price,
                store_name=self.store_name,
                store_url=url,
                image_url=image if image else "",
                category=category,
                sku=sku
            )
        except Exception as e:
            print(f"Error parsing JSON item: {e}")
        return None

    def _get_field(self, item: Dict[str, Any], keys: List[str]) -> Optional[str]:
        """
        Get field value from item using multiple possible keys.

        Args:
            item: Product dictionary
            keys: List of possible key names to try

        Returns:
            Field value or None
        """
        for key in keys:
            if key in item:
                value = item[key]
                # Handle nested objects (e.g., {"price": {"value": 100}})
                if isinstance(value, dict):
                    if 'value' in value:
                        value = value['value']
                    elif 'text' in value:
                        value = value['text']

                if value is not None:
                    return str(value).strip()

        return None

    def _parse_price(self, price_value: Any) -> Optional[float]:
        """
        Parse price from various formats.

        Args:
            price_value: Price value (string, number, or dict)

        Returns:
            Float price or None
        """
        try:
            # Handle dict with value field
            if isinstance(price_value, dict):
                if 'value' in price_value:
                    price_value = price_value['value']
                elif 'amount' in price_value:
                    price_value = price_value['amount']

            # Convert to string and clean
            price_str = str(price_value)
            price_clean = price_str.replace('MXN', '').replace('$', '').replace(',', '').strip()

            return float(price_clean)
        except (ValueError, TypeError):
            return None
