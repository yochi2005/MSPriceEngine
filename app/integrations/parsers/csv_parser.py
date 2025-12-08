"""
CSV Feed Parser for product catalogs.

Supports CSV files from stores with standard product columns.
"""
import csv
from typing import List, Optional, Dict
from ..base import Product
import httpx


class CSVFeedParser:
    """
    Parse CSV product feeds.

    Expected columns (flexible mapping):
    - name/title/product_name
    - price/cost/amount
    - url/link/product_url
    - image/image_url/image_link
    - category/product_category
    - sku/id/product_id
    """

    def __init__(self, store_name: str, column_mapping: Optional[Dict[str, str]] = None):
        """
        Initialize CSV parser.

        Args:
            store_name: Name of the store providing the feed
            column_mapping: Optional custom column mapping
                Example: {'name': 'product_title', 'price': 'cost'}
        """
        self.store_name = store_name
        self.column_mapping = column_mapping or {}

        # Default column mappings (flexible field names)
        self.default_mappings = {
            'name': ['name', 'title', 'product_name', 'product_title'],
            'price': ['price', 'cost', 'amount', 'product_price'],
            'url': ['url', 'link', 'product_url', 'product_link'],
            'image': ['image', 'image_url', 'image_link', 'product_image'],
            'category': ['category', 'product_category', 'product_type'],
            'sku': ['sku', 'id', 'product_id', 'product_sku']
        }

    async def parse_from_url(self, url: str) -> List[Product]:
        """
        Fetch and parse CSV feed from URL.

        Args:
            url: URL of the CSV feed

        Returns:
            List of Product objects
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return self.parse_from_string(response.text)

    def parse_from_file(self, file_path: str) -> List[Product]:
        """
        Parse CSV feed from local file.

        Args:
            file_path: Path to CSV file

        Returns:
            List of Product objects
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return self.parse_from_string(f.read())

    def parse_from_string(self, csv_string: str) -> List[Product]:
        """
        Parse CSV string into products.

        Args:
            csv_string: CSV content as string

        Returns:
            List of Product objects
        """
        products = []
        lines = csv_string.strip().split('\n')

        if not lines:
            return products

        # Parse CSV with DictReader for header support
        reader = csv.DictReader(lines)

        for row in reader:
            product = self._parse_row(row)
            if product:
                products.append(product)

        return products

    def _parse_row(self, row: Dict[str, str]) -> Optional[Product]:
        """Parse a single CSV row into a Product."""
        try:
            # Get column values using flexible mapping
            name = self._get_value(row, 'name')
            price_str = self._get_value(row, 'price')
            url = self._get_value(row, 'url')
            image = self._get_value(row, 'image')
            category = self._get_value(row, 'category')
            sku = self._get_value(row, 'sku')

            # Validate required fields
            if not name or not price_str or not url:
                return None

            # Parse price (remove currency symbols and commas)
            price_clean = price_str.replace('MXN', '').replace('$', '').replace(',', '').strip()
            price = float(price_clean)

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
            print(f"Error parsing CSV row: {e}")
        return None

    def _get_value(self, row: Dict[str, str], field: str) -> Optional[str]:
        """
        Get value from row using flexible column mapping.

        Args:
            row: CSV row as dictionary
            field: Field name to retrieve ('name', 'price', etc.)

        Returns:
            Field value or None
        """
        # Check custom mapping first
        if field in self.column_mapping:
            custom_col = self.column_mapping[field]
            if custom_col in row:
                return row[custom_col].strip()

        # Try default mappings
        if field in self.default_mappings:
            for col_name in self.default_mappings[field]:
                if col_name in row and row[col_name]:
                    return row[col_name].strip()

        # Try exact match
        if field in row:
            return row[field].strip()

        return None
