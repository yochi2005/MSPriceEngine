# Guía de Uso de la API - MSPriceEngine

## Introducción

MSPriceEngine es una API REST que permite buscar y comparar precios de productos en tiendas mexicanas. Esta guía te enseñará cómo usar la API.

## Base URL

```
Development: http://localhost:8000
Production:  https://api.mspriceengine.com (cuando se despliegue)
```

## Autenticación

**Actualmente no requiere autenticación.** Todas las rutas son públicas.

En versiones futuras podrá requerir API key para rate limiting.

## Formato de Respuesta

Todas las respuestas son en formato JSON.

### Respuesta Exitosa
```json
{
  "total": 15,
  "products": [...]
}
```

### Respuesta de Error
```json
{
  "detail": "Product not found"
}
```

## Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | Éxito |
| 404 | Recurso no encontrado |
| 422 | Error de validación (parámetros inválidos) |
| 500 | Error interno del servidor |

---

## Endpoints Disponibles

### 1. Root - Información de la API

**Endpoint:** `GET /`

**Descripción:** Retorna información básica de la API.

**Ejemplo:**
```bash
curl http://localhost:8000/
```

**Respuesta:**
```json
{
  "name": "MSPriceEngine API",
  "version": "0.1.0",
  "description": "Price Search Engine for Mexico",
  "docs": "/docs"
}
```

---

### 2. Health Check

**Endpoint:** `GET /health`

**Descripción:** Verifica que la API esté funcionando.

**Ejemplo:**
```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "healthy"
}
```

---

### 3. Buscar Productos

**Endpoint:** `GET /search`

**Descripción:** Busca productos por nombre.

**Parámetros de Query:**

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `q` | string | ✅ Sí | Término de búsqueda (min 2 caracteres) | `laptop` |
| `store_id` | integer | ❌ No | Filtrar por tienda específica | `1` |
| `min_price` | float | ❌ No | Precio mínimo | `5000` |
| `max_price` | float | ❌ No | Precio máximo | `20000` |
| `limit` | integer | ❌ No | Resultados por página (max 100, default 50) | `20` |
| `offset` | integer | ❌ No | Offset para paginación (default 0) | `0` |

**Ejemplos:**

```bash
# Búsqueda simple
curl "http://localhost:8000/search?q=laptop"

# Búsqueda con filtro de precio
curl "http://localhost:8000/search?q=laptop&min_price=5000&max_price=15000"

# Búsqueda por tienda específica
curl "http://localhost:8000/search?q=iphone&store_id=1"

# Búsqueda con paginación
curl "http://localhost:8000/search?q=laptop&limit=10&offset=0"
```

**Respuesta:**
```json
{
  "total": 15,
  "products": [
    {
      "id": 1,
      "name": "Laptop HP Pavilion Gaming 15-dk1036la",
      "store_id": 1,
      "store_url": "https://amazon.com.mx/dp/B08N5XQWB7",
      "sku": "B08N5XQWB7",
      "price": 12999.99,
      "currency": "MXN",
      "image_url": "https://m.media-amazon.com/images/I/...",
      "available": 1,
      "last_updated": "2024-12-06T18:30:00",
      "created_at": "2024-12-06T10:00:00",
      "store": {
        "id": 1,
        "name": "Amazon MX",
        "url": "https://www.amazon.com.mx",
        "created_at": "2024-12-06T10:00:00"
      }
    },
    {
      "id": 2,
      "name": "Laptop Dell Inspiron 15 3000",
      "price": 8999.99,
      "store": {
        "name": "Walmart MX"
      }
    }
  ]
}
```

---

### 4. Obtener Producto por ID

**Endpoint:** `GET /products/{product_id}`

**Descripción:** Obtiene detalles de un producto específico.

**Parámetros de Ruta:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `product_id` | integer | ID del producto |

**Ejemplo:**
```bash
curl http://localhost:8000/products/1
```

**Respuesta:**
```json
{
  "id": 1,
  "name": "Laptop HP Pavilion Gaming 15-dk1036la",
  "store_id": 1,
  "store_url": "https://amazon.com.mx/dp/B08N5XQWB7",
  "sku": "B08N5XQWB7",
  "price": 12999.99,
  "currency": "MXN",
  "image_url": "https://m.media-amazon.com/images/I/...",
  "available": 1,
  "last_updated": "2024-12-06T18:30:00",
  "created_at": "2024-12-06T10:00:00",
  "store": {
    "id": 1,
    "name": "Amazon MX",
    "url": "https://www.amazon.com.mx",
    "created_at": "2024-12-06T10:00:00"
  }
}
```

**Errores:**
```json
// 404 Not Found
{
  "detail": "Product not found"
}
```

---

### 5. Listar Todas las Tiendas

**Endpoint:** `GET /stores`

**Descripción:** Obtiene lista de todas las tiendas disponibles.

**Ejemplo:**
```bash
curl http://localhost:8000/stores
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Amazon MX",
    "url": "https://www.amazon.com.mx",
    "created_at": "2024-12-06T10:00:00"
  },
  {
    "id": 2,
    "name": "Walmart MX",
    "url": "https://www.walmart.com.mx",
    "created_at": "2024-12-06T10:00:00"
  }
]
```

---

### 6. Obtener Tienda por ID

**Endpoint:** `GET /stores/{store_id}`

**Descripción:** Obtiene información de una tienda específica.

**Parámetros de Ruta:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `store_id` | integer | ID de la tienda |

**Ejemplo:**
```bash
curl http://localhost:8000/stores/1
```

**Respuesta:**
```json
{
  "id": 1,
  "name": "Amazon MX",
  "url": "https://www.amazon.com.mx",
  "created_at": "2024-12-06T10:00:00"
}
```

---

### 7. Productos de una Tienda

**Endpoint:** `GET /stores/{store_id}/products`

**Descripción:** Obtiene todos los productos de una tienda específica.

**Parámetros de Ruta:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `store_id` | integer | ID de la tienda |

**Parámetros de Query:**

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `limit` | integer | Productos por página (max 100) | 50 |
| `offset` | integer | Offset para paginación | 0 |

**Ejemplo:**
```bash
curl "http://localhost:8000/stores/1/products?limit=20"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Laptop HP Pavilion Gaming 15-dk1036la",
    "price": 12999.99,
    "store": {
      "name": "Amazon MX"
    }
  },
  {
    "id": 5,
    "name": "iPhone 14 Pro Max 256GB",
    "price": 24999.00,
    "store": {
      "name": "Amazon MX"
    }
  }
]
```

---

## Ejemplos de Uso

### Python con requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Buscar productos
response = requests.get(f"{BASE_URL}/search", params={"q": "laptop"})
data = response.json()

print(f"Total: {data['total']}")
for product in data['products']:
    print(f"{product['name']} - ${product['price']} ({product['store']['name']})")

# Obtener producto específico
product = requests.get(f"{BASE_URL}/products/1").json()
print(f"Producto: {product['name']}")
```

### JavaScript con fetch

```javascript
const BASE_URL = "http://localhost:8000";

// Buscar productos
async function searchProducts(query) {
  const response = await fetch(`${BASE_URL}/search?q=${query}`);
  const data = await response.json();

  console.log(`Total: ${data.total}`);
  data.products.forEach(product => {
    console.log(`${product.name} - $${product.price} (${product.store.name})`);
  });
}

searchProducts("laptop");
```

### JavaScript con axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
});

// Buscar productos
const searchProducts = async (query, filters = {}) => {
  const response = await api.get('/search', {
    params: { q: query, ...filters }
  });
  return response.data;
};

// Uso
const results = await searchProducts('laptop', {
  min_price: 5000,
  max_price: 15000,
  limit: 10
});

console.log(results.products);
```

### cURL (Terminal)

```bash
# Buscar laptops entre $5,000 y $15,000
curl -X GET "http://localhost:8000/search?q=laptop&min_price=5000&max_price=15000" \
  -H "Accept: application/json"

# Obtener producto ID 1
curl -X GET "http://localhost:8000/products/1" \
  -H "Accept: application/json"

# Listar tiendas
curl -X GET "http://localhost:8000/stores" \
  -H "Accept: application/json"
```

---

## Paginación

Para paginar resultados, usa los parámetros `limit` y `offset`:

```bash
# Página 1 (primeros 20 productos)
curl "http://localhost:8000/search?q=laptop&limit=20&offset=0"

# Página 2 (productos 21-40)
curl "http://localhost:8000/search?q=laptop&limit=20&offset=20"

# Página 3 (productos 41-60)
curl "http://localhost:8000/search?q=laptop&limit=20&offset=40"
```

**Cálculo:**
- `offset = (page - 1) * limit`
- Ejemplo: Página 3 con 20 por página = `(3-1) * 20 = 40`

---

## Documentación Interactiva

La API incluye documentación interactiva en Swagger UI:

**Swagger UI:** http://localhost:8000/docs
**ReDoc:** http://localhost:8000/redoc

Desde Swagger puedes:
- Ver todos los endpoints
- Probar requests directamente
- Ver esquemas de datos
- Descargar OpenAPI spec

---

## Rate Limiting

**Actualmente:** Sin límites

**Futuro:**
- 100 requests/minuto por IP (tier gratuito)
- 1000 requests/minuto con API key (tier premium)

---

## CORS

La API está configurada para aceptar requests desde cualquier origen en desarrollo.

En producción se restringirá a dominios específicos.

---

## Errores Comunes

### Error 422: Validation Error

```json
{
  "detail": [
    {
      "loc": ["query", "q"],
      "msg": "ensure this value has at least 2 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**Solución:** Asegúrate de que el parámetro `q` tenga al menos 2 caracteres.

### Error 404: Not Found

```json
{
  "detail": "Product not found"
}
```

**Solución:** Verifica que el ID del producto exista.

### Error 500: Internal Server Error

**Solución:** Contacta al administrador. Puede ser un error en el servidor.

---

## Buenas Prácticas

1. **Siempre valida las respuestas:**
   ```javascript
   if (response.status === 200) {
     // Procesar datos
   } else {
     // Manejar error
   }
   ```

2. **Usa paginación para muchos resultados:**
   - No hagas queries sin `limit`
   - Usa `limit=20` o `limit=50`

3. **Cachea resultados cuando sea posible:**
   - Los precios se actualizan diariamente
   - Puedes cachear por 1 hora

4. **Maneja errores gracefully:**
   ```python
   try:
       response = requests.get(url)
       response.raise_for_status()
   except requests.exceptions.HTTPError as e:
       print(f"Error: {e}")
   ```

---

## Próximas Features

- `GET /products/{id}/price-history` - Historial de precios
- `GET /products/{id}/compare` - Comparar con productos similares
- `POST /webhooks` - Alertas de precio
- Autenticación con API keys
- GraphQL endpoint

---

## Soporte

- **GitHub Issues:** https://github.com/yochi2005/MSPriceEngine/issues
- **Documentación:** https://github.com/yochi2005/MSPriceEngine/tree/main/docs
- **Email:** (pendiente)

---

**Última actualización:** 6 de diciembre de 2024
**Versión de la API:** 0.1.0
