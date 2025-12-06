"""Base scraper class - all scrapers inherit from this."""
import httpx
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all store scrapers."""

    def __init__(self, store_name: str, base_url: str):
        """
        Initialize scraper.

        Args:
            store_name: Name of the store (e.g., "Amazon MX")
            base_url: Base URL of the store
        """
        self.store_name = store_name
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    async def fetch(self, url: str, retry: int = 3) -> Optional[str]:
        """
        Fetch HTML content from URL.

        Args:
            url: URL to fetch
            retry: Number of retries on failure

        Returns:
            HTML content as string, or None if failed
        """
        for attempt in range(retry):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(url, headers=self.headers, follow_redirects=True)
                    response.raise_for_status()
                    logger.info(f"Successfully fetched {url}")
                    return response.text
            except httpx.HTTPError as e:
                logger.warning(f"Attempt {attempt + 1}/{retry} failed for {url}: {e}")
                if attempt < retry - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {retry} attempts")
                    return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content with BeautifulSoup.

        Args:
            html: HTML content as string

        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'lxml')

    def clean_price(self, price_text: str) -> Optional[float]:
        """
        Clean and convert price text to float.

        Examples:
            "$1,299.99" -> 1299.99
            "$ 1299" -> 1299.0
            "MXN 1,299.99" -> 1299.99

        Args:
            price_text: Raw price text

        Returns:
            Price as float, or None if parsing failed
        """
        try:
            # Remove currency symbols, commas, and spaces
            cleaned = price_text.replace('$', '').replace(',', '').replace(' ', '').replace('MXN', '').strip()
            return float(cleaned)
        except (ValueError, AttributeError):
            logger.warning(f"Failed to parse price: {price_text}")
            return None

    def clean_name(self, name: str) -> str:
        """
        Clean product name.

        Args:
            name: Raw product name

        Returns:
            Cleaned product name
        """
        return ' '.join(name.split()).strip()

    @abstractmethod
    async def scrape_search(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Scrape search results for a query.

        This method must be implemented by each specific scraper.

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            List of product dictionaries with keys:
                - name: str
                - price: float
                - url: str
                - sku: str (optional)
                - image_url: str (optional)
                - available: bool
        """
        pass

    @abstractmethod
    async def scrape_product(self, url: str) -> Optional[Dict]:
        """
        Scrape details of a single product.

        This method must be implemented by each specific scraper.

        Args:
            url: Product URL

        Returns:
            Product dictionary or None if failed
        """
        pass

    async def scrape_multiple(self, urls: List[str]) -> List[Dict]:
        """
        Scrape multiple product URLs concurrently.

        Args:
            urls: List of product URLs

        Returns:
            List of product dictionaries
        """
        tasks = [self.scrape_product(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]
