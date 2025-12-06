"""Scraper modules for different stores."""
from .base import BaseScraper
from .amazon import AmazonScraper
from .walmart import WalmartScraper
from .liverpool import LiverpoolScraper

__all__ = [
    "BaseScraper",
    "AmazonScraper",
    "WalmartScraper",
    "LiverpoolScraper"
]
