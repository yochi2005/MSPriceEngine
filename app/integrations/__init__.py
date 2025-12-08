"""
Integrations module for external data sources.

This module replaces the old scraping approach with structured data sources:
- Official store APIs
- XML/CSV/JSON feeds
- Structured product catalogs
"""
from .base import BaseIntegration, Product as IntegrationProduct

__all__ = ['BaseIntegration', 'IntegrationProduct']
