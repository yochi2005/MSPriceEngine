"""
API Adapter for official store REST APIs.

Handles authentication, rate limiting, and response parsing.
"""
import httpx
from typing import List, Optional, Dict, Any, Callable
from abc import ABC, abstractmethod
from .base import BaseIntegration, Product
import asyncio
from datetime import datetime, timedelta


class APIAdapter(BaseIntegration):
    """
    Base adapter for REST API integrations.

    Provides common functionality for API calls:
    - Authentication (API keys, OAuth, etc.)
    - Rate limiting
    - Error handling
    - Response parsing
    """

    def __init__(
        self,
        store_name: str,
        config: Optional[Dict[str, Any]] = None,
        base_url: str = "",
        auth_type: str = "none",
        rate_limit: int = 10
    ):
        """
        Initialize API adapter.

        Args:
            store_name: Name of the store
            config: Configuration dictionary (API keys, tokens, etc.)
            base_url: Base URL for the API
            auth_type: Authentication type ('none', 'api_key', 'bearer', 'oauth')
            rate_limit: Maximum requests per second
        """
        super().__init__(store_name, config)
        self.base_url = base_url.rstrip('/')
        self.auth_type = auth_type
        self.rate_limit = rate_limit

        # Rate limiting
        self._request_times: List[datetime] = []
        self._rate_limit_lock = asyncio.Lock()

    async def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated API request with rate limiting.

        Args:
            endpoint: API endpoint (e.g., '/products/search')
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            headers: Additional headers
            data: Request body data

        Returns:
            Parsed JSON response
        """
        # Apply rate limiting
        await self._apply_rate_limit()

        # Build URL
        url = f"{self.base_url}{endpoint}"

        # Prepare headers with authentication
        request_headers = self._get_auth_headers()
        if headers:
            request_headers.update(headers)

        # Make request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                headers=request_headers,
                json=data
            )
            response.raise_for_status()
            return response.json()

    def _get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers based on auth_type.

        Returns:
            Dictionary of authentication headers
        """
        headers = {
            'User-Agent': 'MSPriceEngine/1.0',
            'Accept': 'application/json'
        }

        if self.auth_type == 'api_key':
            api_key = self.config.get('api_key')
            if api_key:
                # Common patterns for API key authentication
                key_header = self.config.get('api_key_header', 'X-API-Key')
                headers[key_header] = api_key

        elif self.auth_type == 'bearer':
            token = self.config.get('token') or self.config.get('access_token')
            if token:
                headers['Authorization'] = f'Bearer {token}'

        elif self.auth_type == 'oauth':
            # OAuth typically requires more complex flow
            # Subclasses should override this for specific OAuth implementations
            token = self.config.get('access_token')
            if token:
                headers['Authorization'] = f'Bearer {token}'

        return headers

    async def _apply_rate_limit(self):
        """Apply rate limiting to API requests."""
        async with self._rate_limit_lock:
            now = datetime.now()

            # Remove request times older than 1 second
            cutoff = now - timedelta(seconds=1)
            self._request_times = [t for t in self._request_times if t > cutoff]

            # If we're at the rate limit, wait
            if len(self._request_times) >= self.rate_limit:
                oldest = self._request_times[0]
                wait_time = 1 - (now - oldest).total_seconds()
                if wait_time > 0:
                    await asyncio.sleep(wait_time)

            # Record this request
            self._request_times.append(datetime.now())

    @abstractmethod
    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        """
        Fetch products from the API.

        Subclasses must implement this with store-specific logic.
        """
        pass

    async def test_connection(self) -> bool:
        """
        Test API connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try a simple API call to test connection
            # Subclasses should override with appropriate test endpoint
            await self.fetch_products(query="test", limit=1)
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False


class PaginatedAPIAdapter(APIAdapter):
    """
    API Adapter with pagination support.

    Handles APIs that return paginated results.
    """

    async def fetch_all_pages(
        self,
        endpoint: str,
        params: Dict[str, Any],
        response_parser: Callable[[Dict[str, Any]], List[Product]],
        max_pages: int = 10,
        page_key: str = "page",
        page_size_key: str = "limit"
    ) -> List[Product]:
        """
        Fetch all pages from a paginated API.

        Args:
            endpoint: API endpoint
            params: Base query parameters
            response_parser: Function to parse response into Products
            max_pages: Maximum number of pages to fetch
            page_key: Parameter name for page number
            page_size_key: Parameter name for page size

        Returns:
            List of all products from all pages
        """
        all_products = []
        page = 1

        while page <= max_pages:
            # Set pagination params
            page_params = params.copy()
            page_params[page_key] = page

            # Make request
            try:
                response = await self._make_request(endpoint, params=page_params)
                products = response_parser(response)

                if not products:
                    # No more results
                    break

                all_products.extend(products)

                # Check if there are more pages
                # Common patterns: has_next, total_pages, next_page, etc.
                if not self._has_more_pages(response, page):
                    break

                page += 1

            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break

        return all_products

    def _has_more_pages(self, response: Dict[str, Any], current_page: int) -> bool:
        """
        Check if there are more pages to fetch.

        Args:
            response: API response
            current_page: Current page number

        Returns:
            True if more pages available
        """
        # Try common pagination patterns
        if 'has_next' in response:
            return response['has_next']

        if 'next_page' in response:
            return response['next_page'] is not None

        if 'total_pages' in response:
            return current_page < response['total_pages']

        if 'paging' in response:
            paging = response['paging']
            if 'next' in paging:
                return paging['next'] is not None
            if 'total_pages' in paging:
                return current_page < paging['total_pages']

        # Default: assume no more pages if we can't determine
        return False
