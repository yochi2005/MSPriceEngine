# Integrations Module

Sistema de integraciones para obtener productos de tiendas mediante APIs oficiales y feeds estructurados.

## 🎯 Objetivo

Reemplazar el web scraping con métodos más confiables y escalables:
- APIs oficiales de tiendas
- Feeds XML/CSV/JSON estructurados
- Validación automática de productos

## 📁 Estructura

```
integrations/
├── base.py                 # Clases base: BaseIntegration, Product
├── api_adapter.py          # Adaptador para APIs REST con rate limiting
├── parsers/
│   ├── xml_parser.py       # Parser XML (Google Merchant, genérico)
│   ├── csv_parser.py       # Parser CSV con mapeo flexible
│   └── json_parser.py      # Parser JSON con auto-detección
└── stores/
    ├── mercadolibre.py     # ✅ Mercado Libre API (listo)
    ├── coppel.py           # ⚠️ Coppel JSON (requiere feed_url)
    └── sears.py            # ⚠️ Sears XML (requiere feed_url)
```

## 🚀 Quick Start

### Mercado Libre (API):

```python
from app.integrations.stores.mercadolibre import MercadoLibreIntegration

ml = MercadoLibreIntegration()
products = await ml.fetch_products(query="laptop", limit=50)
```

### Coppel (JSON Feed):

```python
from app.integrations.stores.coppel import CoppelIntegration

config = {'feed_url': 'https://coppel.com/api/products.json'}
coppel = CoppelIntegration(config=config)
products = await coppel.fetch_products(query="laptop")
```

### Sears (XML Feed):

```python
from app.integrations.stores.sears import SearsIntegration

config = {'feed_url': 'https://sears.com.mx/feed/products.xml'}
sears = SearsIntegration(config=config)
products = await sears.fetch_products(query="tv")
```

## 🏗️ Crear Nueva Integración

### Opción 1: API REST

```python
from app.integrations.api_adapter import APIAdapter
from app.integrations.base import Product

class MiTiendaIntegration(APIAdapter):
    def __init__(self, config=None):
        super().__init__(
            store_name="Mi Tienda",
            config=config or {},
            base_url="https://api.mitienda.com",
            auth_type="api_key",
            rate_limit=10
        )

    async def fetch_products(self, query=None, category=None, limit=100):
        response = await self._make_request('/search', params={'q': query})
        # Parsear y retornar productos...
```

### Opción 2: Feed JSON/XML/CSV

```python
from app.integrations.base import BaseIntegration
from app.integrations.parsers.json_parser import JSONFeedParser

class MiTiendaIntegration(BaseIntegration):
    def __init__(self, config=None):
        super().__init__(store_name="Mi Tienda", config=config)
        self.parser = JSONFeedParser(store_name=self.store_name)

    async def fetch_products(self, query=None, category=None, limit=100):
        products = await self.parser.parse_from_url(self.config['feed_url'])
        return self.validate_products(products)[:limit]
```

## ✅ Características

### BaseIntegration
- ✅ Estructura estandarizada de productos
- ✅ Validación automática
- ✅ Interfaz consistente

### APIAdapter
- ✅ Rate limiting automático
- ✅ Autenticación (API Key, Bearer, OAuth)
- ✅ Manejo de errores
- ✅ Paginación automática

### Parsers
- ✅ XML: Google Merchant Center + genérico
- ✅ CSV: Mapeo flexible de columnas
- ✅ JSON: Auto-detección de estructura

## 📊 Estructura de Product

```python
@dataclass
class Product:
    name: str               # Nombre del producto
    price: float            # Precio (MXN por defecto)
    store_name: str         # Nombre de la tienda
    store_url: str          # URL del producto
    image_url: str          # URL de la imagen
    category: Optional[str] # Categoría (opcional)
    sku: Optional[str]      # SKU/ID único (opcional)
    currency: str = "MXN"   # Moneda
    available: bool = True  # Disponibilidad
```

## 🧪 Testing

Ejecutar pruebas:

```bash
cd /home/yochi/Documents/MSPriceEngine
source venv/bin/activate
python test_integrations.py
```

## 📚 Documentación Completa

Ver `docs/INTEGRATION_GUIDE.md` para:
- Guía completa de uso
- Ejemplos detallados
- Configuración de autenticación
- Troubleshooting

## 🔑 Configuración

### Variables de Entorno (recomendado):

```bash
# .env
MERCADOLIBRE_API_KEY=optional
COPPEL_FEED_URL=https://coppel.com/api/feed.json
SEARS_FEED_URL=https://sears.com.mx/feed.xml
```

### Configuración en Código:

```python
config = {
    'api_key': 'tu-api-key',
    'feed_url': 'https://...',
    'rate_limit': 5
}
```

## ⚠️ Notas Importantes

1. **Mercado Libre** está listo para usar (no requiere configuración)
2. **Coppel** y **Sears** requieren URLs de feeds (pendientes de obtener)
3. Siempre validar productos antes de guardar en DB
4. Respetar rate limits para evitar bloqueos
5. NO usar web scraping si hay API o feed disponible

## 🎯 Estado de Integraciones

| Tienda | Método | Estado | Notas |
|--------|--------|--------|-------|
| Mercado Libre | API REST | ✅ Listo | Público, sin auth |
| Coppel | JSON Feed | ⚠️ Config | Requiere feed_url |
| Sears | XML Feed | ⚠️ Config | Requiere feed_url |
| Amazon MX | - | 🔴 Pendiente | Por implementar |
| Walmart MX | - | 🔴 Pendiente | Por implementar |
| Liverpool | - | 🔴 Pendiente | Por implementar |
| Best Buy MX | - | 🔴 Pendiente | Por implementar |

## 🚀 Próximos Pasos

1. Obtener URLs de feeds para Coppel y Sears
2. Implementar integraciones restantes
3. Crear endpoint de sincronización automática
4. Agregar sistema de caché para feeds
5. Implementar actualización programada de catálogos
