"""Amazon Mexico scraper."""
from typing import List, Dict, Optional
import logging
from urllib.parse import quote_plus
from .base import BaseScraper

logger = logging.getLogger(__name__)


class AmazonScraper(BaseScraper):
    """Scraper for Amazon Mexico."""

    def __init__(self):
        super().__init__(
            store_name="Amazon MX",
            base_url="https://www.amazon.com.mx"
        )

    async def scrape_search(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Scrape Amazon MX search results.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of product dictionaries
        """
        search_url = f"{self.base_url}/s?k={quote_plus(query)}"
        logger.info(f"Scraping Amazon MX search: {search_url}")

        html = await self.fetch(search_url)
        if not html:
            return []

        soup = self.parse_html(html)
        products = []

        # Amazon uses div[data-component-type="s-search-result"]
        result_items = soup.find_all('div', {'data-component-type': 's-search-result'}, limit=max_results)

        for item in result_items:
            try:
                product = self._parse_search_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Failed to parse Amazon search item: {e}")
                continue

        logger.info(f"Found {len(products)} products on Amazon MX")
        return products

    def _parse_search_item(self, item) -> Optional[Dict]:
        """Parse a single search result item."""
        try:
            # Product name
            name_elem = item.find('h2', class_='s-line-clamp-2')
            if not name_elem:
                return None
            name = self.clean_name(name_elem.get_text())

            # Product URL
            link_elem = item.find('a', class_='a-link-normal s-no-outline')
            if not link_elem or not link_elem.get('href'):
                return None
            url = self.base_url + link_elem['href'].split('?')[0]  # Remove query params

            # Price - Amazon has multiple price formats
            price = None
            price_whole = item.find('span', class_='a-price-whole')
            price_fraction = item.find('span', class_='a-price-fraction')

            if price_whole:
                price_text = price_whole.get_text() + (price_fraction.get_text() if price_fraction else '00')
                price = self.clean_price(price_text)

            if not price:
                return None

            # Image URL
            image_elem = item.find('img', class_='s-image')
            image_url = image_elem.get('src') if image_elem else None

            # SKU (ASIN)
            asin = item.get('data-asin')

            return {
                'name': name,
                'price': price,
                'url': url,
                'sku': asin,
                'image_url': image_url,
                'available': True
            }

        except Exception as e:
            logger.warning(f"Error parsing Amazon item: {e}")
            return None

    async def scrape_product(self, url: str) -> Optional[Dict]:
        """
        Scrape a single Amazon product page.

        Args:
            url: Product URL

        Returns:
            Product dictionary or None
        """
        logger.info(f"Scraping Amazon product: {url}")

        html = await self.fetch(url)
        if not html:
            return None

        soup = self.parse_html(html)

        try:
            # Product name
            name_elem = soup.find('span', id='productTitle')
            if not name_elem:
                return None
            name = self.clean_name(name_elem.get_text())

            # Price
            price = None
            price_elem = soup.find('span', class_='a-price-whole')
            if price_elem:
                price_fraction = soup.find('span', class_='a-price-fraction')
                price_text = price_elem.get_text() + (price_fraction.get_text() if price_fraction else '00')
                price = self.clean_price(price_text)

            if not price:
                return None

            # Image
            image_elem = soup.find('img', id='landingImage')
            image_url = image_elem.get('src') if image_elem else None

            # ASIN
            asin = None
            asin_elem = soup.find('input', {'id': 'ASIN'})
            if asin_elem:
                asin = asin_elem.get('value')

            # Availability
            available = True
            availability_elem = soup.find('div', id='availability')
            if availability_elem:
                availability_text = availability_elem.get_text().lower()
                available = 'no disponible' not in availability_text and 'out of stock' not in availability_text

            return {
                'name': name,
                'price': price,
                'url': url,
                'sku': asin,
                'image_url': image_url,
                'available': available
            }

        except Exception as e:
            logger.error(f"Error scraping Amazon product {url}: {e}")
            return None
