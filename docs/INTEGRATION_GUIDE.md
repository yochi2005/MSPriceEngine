# Integration Guide - APIs and Feeds

Este documento explica cómo usar el nuevo sistema de integraciones para obtener productos de tiendas mediante APIs oficiales y feeds estructurados (XML/CSV/JSON).

## 🎯 Cambio de Enfoque

**Antes:** Scraping HTML (lento, frágil, difícil de mantener)
**Ahora:** APIs oficiales y feeds estructurados (rápido, confiable, escalable)

## 📋 Prioridad de Métodos

1. **APIs Oficiales** - Siempre preferir si está disponible
2. **Feeds XML/CSV/JSON** - Segunda opción para catálogos estructurados
3. **Web Scraping** - SOLO como último recurso (no recomendado)

---

## 🏗️ Arquitectura del Sistema

```
app/integrations/
├── base.py                    # Clases base: BaseIntegration, Product
├── api_adapter.py             # Adaptador para APIs REST
├── parsers/
│   ├── xml_parser.py          # Parser para feeds XML
│   ├── csv_parser.py          # Parser para feeds CSV
│   └── json_parser.py         # Parser para feeds JSON
└── stores/
    ├── mercadolibre.py        # Integración Mercado Libre API
    ├── coppel.py              # Integración Coppel (JSON feed)
    └── sears.py               # Integración Sears (XML feed)
```

---

## 🚀 Integraciones Disponibles

### 1. Mercado Libre (API Oficial)

**Estado:** ✅ Implementado y listo para usar
**Método:** API REST pública (sin autenticación requerida)
**Documentación:** https://developers.mercadolibre.com.mx/

#### Uso Básico:

```python
from app.integrations.stores.mercadolibre import MercadoLibreIntegration

# Inicializar
ml = MercadoLibreIntegration()

# Buscar productos
products = await ml.fetch_products(query="laptop", limit=50)

# Probar conexión
is_connected = await ml.test_connection()

# Obtener categorías
categories = await ml.get_categories()
```

#### Características:
- ✅ Búsqueda por texto
- ✅ Filtrado por categoría
- ✅ Paginación automática
- ✅ Imágenes de alta resolución
- ✅ Precios en tiempo real
- ✅ Rate limiting automático (5 req/s)

---

### 2. Coppel (JSON Feed)

**Estado:** ⚠️ Implementado (requiere configuración)
**Método:** Feed JSON estructurado
**URL del Feed:** *Pendiente de obtener de Coppel*

#### Configuración:

```python
from app.integrations.stores.coppel import CoppelIntegration

# Configurar con URL del feed
config = {
    'feed_url': 'https://coppel.com/api/products.json',  # URL real pendiente
    'product_path': 'data.products'  # Opcional: ruta a productos en JSON
}

coppel = CoppelIntegration(config=config)
products = await coppel.fetch_products(query="laptop")
```

#### Características:
- ✅ Soporte para JSON anidado
- ✅ Mapeo flexible de campos
- ✅ Filtrado local por query y categoría
- ✅ Validación automática de productos

#### Formatos JSON Soportados:

```json
// Formato 1: Array directo
[
  {"name": "Laptop HP", "price": 12999, "url": "...", "image": "..."},
  ...
]

// Formato 2: Objeto con array "products"
{
  "products": [
    {"name": "Laptop HP", "price": 12999, ...}
  ]
}

// Formato 3: Anidado (usar product_path)
{
  "data": {
    "items": [
      {"name": "Laptop HP", "price": 12999, ...}
    ]
  }
}
```

---

### 3. Sears (XML Feed)

**Estado:** ⚠️ Implementado (requiere configuración)
**Método:** Feed XML (Google Merchant Center o genérico)
**URL del Feed:** *Pendiente de obtener de Sears*

#### Configuración:

```python
from app.integrations.stores.sears import SearsIntegration

# Configurar con URL del feed
config = {
    'feed_url': 'https://sears.com.mx/feed/products.xml'  # URL real pendiente
}

sears = SearsIntegration(config=config)
products = await sears.fetch_products(query="televisor")
```

#### Características:
- ✅ Google Merchant Center XML
- ✅ Formato XML genérico
- ✅ Auto-detección de formato
- ✅ Filtrado local

#### Formatos XML Soportados:

```xml
<!-- Formato 1: Google Merchant Center -->
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <g:title>Laptop HP 15</g:title>
    <g:price>12999 MXN</g:price>
    <g:link>https://...</g:link>
    <g:image_link>https://...</g:image_link>
  </entry>
</feed>

<!-- Formato 2: XML Genérico -->
<products>
  <product>
    <name>Laptop HP 15</name>
    <price>12999</price>
    <url>https://...</url>
    <image>https://...</image>
  </product>
</products>
```

---

## 🔧 Crear Nueva Integración

### Paso 1: Para API REST

```python
# app/integrations/stores/nueva_tienda.py
from typing import List, Optional, Dict, Any
from ..api_adapter import APIAdapter
from ..base import Product

class NuevaTiendaIntegration(APIAdapter):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            store_name="Nueva Tienda",
            config=config or {},
            base_url="https://api.nuevatienda.com",
            auth_type="api_key",  # o "bearer", "oauth", "none"
            rate_limit=10  # requests por segundo
        )

    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        # Construir parámetros
        params = {
            'q': query,
            'limit': limit
        }

        # Hacer request
        response = await self._make_request('/products/search', params=params)

        # Parsear respuesta
        products = []
        for item in response.get('items', []):
            product = Product(
                name=item['name'],
                price=float(item['price']),
                store_name=self.store_name,
                store_url=item['url'],
                image_url=item['image'],
                category=item.get('category'),
                sku=item.get('id')
            )
            products.append(product)

        return self.validate_products(products)
```

### Paso 2: Para Feed JSON

```python
from ..base import BaseIntegration, Product
from ..parsers.json_parser import JSONFeedParser

class NuevaTiendaIntegration(BaseIntegration):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(store_name="Nueva Tienda", config=config)
        self.feed_url = self.config.get('feed_url', '')
        self.parser = JSONFeedParser(
            store_name=self.store_name,
            product_path=self.config.get('product_path')
        )

    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        products = await self.parser.parse_from_url(self.feed_url)

        # Filtrar localmente
        if query:
            products = [p for p in products if query.lower() in p.name.lower()]

        return self.validate_products(products)[:limit]
```

### Paso 3: Para Feed XML

```python
from ..base import BaseIntegration, Product
from ..parsers.xml_parser import XMLFeedParser

class NuevaTiendaIntegration(BaseIntegration):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(store_name="Nueva Tienda", config=config)
        self.feed_url = self.config.get('feed_url', '')
        self.parser = XMLFeedParser(store_name=self.store_name)

    async def fetch_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        products = await self.parser.parse_from_url(self.feed_url)

        # Filtrar localmente
        if query:
            products = [p for p in products if query.lower() in p.name.lower()]

        return self.validate_products(products)[:limit]
```

---

## 🧪 Testing

### Probar Integración:

```python
import asyncio
from app.integrations.stores.mercadolibre import MercadoLibreIntegration

async def test():
    ml = MercadoLibreIntegration()

    # Test conexión
    print("Testing connection...")
    connected = await ml.test_connection()
    print(f"Connected: {connected}")

    # Buscar productos
    print("\nFetching products...")
    products = await ml.fetch_products(query="laptop", limit=5)

    for p in products:
        print(f"- {p.name}: ${p.price} MXN")
        print(f"  URL: {p.store_url}")
        print(f"  Image: {p.image_url}")
        print()

# Ejecutar
asyncio.run(test())
```

---

## 📊 Validación de Productos

Todos los productos pasan por validación automática:

```python
class Product:
    def validate(self) -> bool:
        # ✅ Nombre no vacío
        if not self.name or len(self.name.strip()) == 0:
            return False

        # ✅ Precio válido (> 0)
        if not self.price or self.price <= 0:
            return False

        # ✅ URL válida (empieza con http)
        if not self.store_url or not self.store_url.startswith('http'):
            return False

        # ✅ Imagen válida (empieza con http)
        if not self.image_url or not self.image_url.startswith('http'):
            return False

        return True
```

---

## 🔑 Configuración de APIs

### Autenticación API Key:

```python
config = {
    'api_key': 'tu-api-key-aqui',
    'api_key_header': 'X-API-Key'  # Opcional, default: 'X-API-Key'
}

integration = NuevaTiendaIntegration(config=config)
```

### Autenticación Bearer Token:

```python
config = {
    'access_token': 'tu-token-aqui'
}

integration = NuevaTiendaIntegration(config=config)
```

### Autenticación OAuth:

```python
config = {
    'access_token': 'tu-oauth-token-aqui'
}

integration = NuevaTiendaIntegration(config=config)
```

---

## ⚡ Rate Limiting

El sistema incluye rate limiting automático para evitar bloqueos:

```python
# Configurar límite personalizado
integration = APIAdapter(
    store_name="Mi Tienda",
    base_url="https://api.mitienda.com",
    rate_limit=5  # máximo 5 requests por segundo
)
```

El rate limiting:
- ✅ Aplica automáticamente delays
- ✅ Previene bloqueos por exceso de requests
- ✅ Thread-safe (usa asyncio.Lock)

---

## 🎯 Próximos Pasos

1. **Obtener URLs de Feeds:**
   - Contactar a Coppel para feed JSON
   - Contactar a Sears para feed XML

2. **Nuevas Integraciones:**
   - Best Buy Mexico (API o feed pendiente)
   - Otras tiendas según necesidad

3. **Integrar con Base de Datos:**
   - Crear endpoint para importar productos
   - Sincronización automática de catálogos

---

## 📝 Notas Importantes

- **NO usar web scraping** a menos que sea absolutamente necesario
- Respetar términos de servicio de cada tienda
- Usar rate limiting apropiado
- Validar siempre los productos antes de guardar
- Mantener configuraciones sensibles (API keys) en variables de entorno

---

## ❓ Troubleshooting

### Error: "feed_url not configured"
**Solución:** Pasar config con feed_url al inicializar:
```python
config = {'feed_url': 'https://...'}
integration = CoppelIntegration(config=config)
```

### Error: "Connection test failed"
**Solución:** Verificar:
- URL del feed/API es correcta
- Hay conexión a internet
- API key es válida (si se requiere)

### Error: "Rate limit exceeded"
**Solución:** Reducir rate_limit o agregar delays entre requests.

---

## 📚 Referencias

- **Mercado Libre API:** https://developers.mercadolibre.com.mx/
- **Google Merchant Center XML:** https://support.google.com/merchants/answer/7052112
- **BaseIntegration:** Ver `app/integrations/base.py`
- **API Adapter:** Ver `app/integrations/api_adapter.py`
