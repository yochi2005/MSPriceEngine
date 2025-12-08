"""
Store-specific integrations.

Each file implements integration for a specific store using APIs or feeds.
"""
from .mercadolibre import MercadoLibreIntegration
from .coppel import CoppelIntegration
from .sears import SearsIntegration
from .amazon import AmazonMXIntegration
from .walmart import WalmartMXIntegration
from .liverpool import LiverpoolIntegration

__all__ = [
    'MercadoLibreIntegration',
    'CoppelIntegration',
    'SearsIntegration',
    'AmazonMXIntegration',
    'WalmartMXIntegration',
    'LiverpoolIntegration'
]
