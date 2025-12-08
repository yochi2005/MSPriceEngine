"""
XML Feed Parser for product catalogs.

Supports standard XML formats from stores like Sears.
"""
import xml.etree.ElementTree as ET
from typing import List, Optional, Dict
from ..base import Product
import httpx


class XMLFeedParser:
    """
    Parse XML product feeds.

    Common XML formats supported:
    - Google Merchant Center XML
    - Custom store XML feeds
    """

    def __init__(self, store_name: str):
        """
        Initialize XML parser.

        Args:
            store_name: Name of the store providing the feed
        """
        self.store_name = store_name

    async def parse_from_url(self, url: str) -> List[Product]:
        """
        Fetch and parse XML feed from URL.

        Args:
            url: URL of the XML feed

        Returns:
            List of Product objects
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return self.parse_from_string(response.text)

    def parse_from_file(self, file_path: str) -> List[Product]:
        """
        Parse XML feed from local file.

        Args:
            file_path: Path to XML file

        Returns:
            List of Product objects
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return self.parse_from_string(f.read())

    def parse_from_string(self, xml_string: str) -> List[Product]:
        """
        Parse XML string into products.

        Args:
            xml_string: XML content as string

        Returns:
            List of Product objects
        """
        root = ET.fromstring(xml_string)
        products = []

        # Try Google Merchant Center format
        for item in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            product = self._parse_google_merchant_item(item)
            if product:
                products.append(product)

        # Try generic XML format
        if not products:
            for item in root.findall('.//product'):
                product = self._parse_generic_item(item)
                if product:
                    products.append(product)

        return products

    def _parse_google_merchant_item(self, item: ET.Element) -> Optional[Product]:
        """Parse Google Merchant Center XML format."""
        try:
            # Namespace for Google Merchant Center
            ns = {'g': 'http://base.google.com/ns/1.0'}

            name = item.find('.//g:title', ns)
            price_elem = item.find('.//g:price', ns)
            link = item.find('.//g:link', ns)
            image = item.find('.//g:image_link', ns)
            category = item.find('.//g:product_type', ns)
            sku = item.find('.//g:id', ns)

            if name is not None and price_elem is not None:
                # Extract price (remove currency symbol)
                price_text = price_elem.text.replace('MXN', '').replace('$', '').replace(',', '').strip()
                price = float(price_text)

                return Product(
                    name=name.text,
                    price=price,
                    store_name=self.store_name,
                    store_url=link.text if link is not None else "",
                    image_url=image.text if image is not None else "",
                    category=category.text if category is not None else None,
                    sku=sku.text if sku is not None else None
                )
        except Exception as e:
            print(f"Error parsing Google Merchant item: {e}")
        return None

    def _parse_generic_item(self, item: ET.Element) -> Optional[Product]:
        """Parse generic XML format."""
        try:
            name = item.find('name')
            price_elem = item.find('price')
            link = item.find('url')
            image = item.find('image')
            category = item.find('category')
            sku = item.find('sku')

            if name is not None and price_elem is not None:
                price = float(price_elem.text.replace('$', '').replace(',', '').strip())

                return Product(
                    name=name.text,
                    price=price,
                    store_name=self.store_name,
                    store_url=link.text if link is not None else "",
                    image_url=image.text if image is not None else "",
                    category=category.text if category is not None else None,
                    sku=sku.text if sku is not None else None
                )
        except Exception as e:
            print(f"Error parsing generic XML item: {e}")
        return None
