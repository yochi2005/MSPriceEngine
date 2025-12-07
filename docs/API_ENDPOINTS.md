# API Endpoints Reference - MSPriceEngine

## Base URL
```
http://localhost:8000
```

## Quick Reference Table

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/` | Info de la API | No |
| GET | `/health` | Health check | No |
| GET | `/search` | Buscar productos | No |
| GET | `/products/{id}` | Detalle de producto | No |
| GET | `/stores` | Listar tiendas | No |
| GET | `/stores/{id}` | Detalle de tienda | No |
| GET | `/stores/{id}/products` | Productos de tienda | No |

---

## GET /

**Descripción:** Información básica de la API

**Response:**
```json
{
  "name": "MSPriceEngine API",
  "version": "0.1.0",
  "description": "Price Search Engine for Mexico",
  "docs": "/docs"
}
```

---

## GET /health

**Descripción:** Verificar estado de la API

**Response:**
```json
{
  "status": "healthy"
}
```

---

## GET /search

**Descripción:** Buscar productos

**Query Parameters:**

| Parámetro | Tipo | Requerido | Validación | Default | Ejemplo |
|-----------|------|-----------|------------|---------|---------|
| q | string | ✅ | min_length=2 | - | laptop |
| store_id | integer | ❌ | - | None | 1 |
| min_price | float | ❌ | >= 0 | None | 5000 |
| max_price | float | ❌ | >= 0 | None | 20000 |
| limit | integer | ❌ | 1-100 | 50 | 20 |
| offset | integer | ❌ | >= 0 | 0 | 0 |

**Example Request:**
```
GET /search?q=laptop&min_price=5000&max_price=15000&limit=20&offset=0
```

**Response 200:**
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
      "image_url": "https://...",
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
  ]
}
```

**Response 422 (Validation Error):**
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

---

## GET /products/{product_id}

**Descripción:** Obtener detalle de un producto

**Path Parameters:**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| product_id | integer | ✅ | ID del producto |

**Example Request:**
```
GET /products/1
```

**Response 200:**
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

**Response 404:**
```json
{
  "detail": "Product not found"
}
```

---

## GET /stores

**Descripción:** Listar todas las tiendas

**Example Request:**
```
GET /stores
```

**Response 200:**
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
  },
  {
    "id": 3,
    "name": "Liverpool",
    "url": "https://www.liverpool.com.mx",
    "created_at": "2024-12-06T10:00:00"
  }
]
```

---

## GET /stores/{store_id}

**Descripción:** Obtener detalle de una tienda

**Path Parameters:**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| store_id | integer | ✅ | ID de la tienda |

**Example Request:**
```
GET /stores/1
```

**Response 200:**
```json
{
  "id": 1,
  "name": "Amazon MX",
  "url": "https://www.amazon.com.mx",
  "created_at": "2024-12-06T10:00:00"
}
```

**Response 404:**
```json
{
  "detail": "Store not found"
}
```

---

## GET /stores/{store_id}/products

**Descripción:** Obtener productos de una tienda específica

**Path Parameters:**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| store_id | integer | ✅ | ID de la tienda |

**Query Parameters:**

| Parámetro | Tipo | Requerido | Validación | Default |
|-----------|------|-----------|------------|---------|
| limit | integer | ❌ | 1-100 | 50 |
| offset | integer | ❌ | >= 0 | 0 |

**Example Request:**
```
GET /stores/1/products?limit=20&offset=0
```

**Response 200:**
```json
[
  {
    "id": 1,
    "name": "Laptop HP Pavilion Gaming 15-dk1036la",
    "store_id": 1,
    "store_url": "https://amazon.com.mx/dp/B08N5XQWB7",
    "sku": "B08N5XQWB7",
    "price": 12999.99,
    "currency": "MXN",
    "image_url": "https://...",
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
]
```

**Response 404:**
```json
{
  "detail": "Store not found"
}
```

---

## Response Schemas

### ProductSearchResponse

```typescript
{
  total: integer,         // Total de productos encontrados
  products: Product[]     // Array de productos
}
```

### Product

```typescript
{
  id: integer,
  name: string,
  store_id: integer,
  store_url: string,
  sku: string | null,
  price: float,
  currency: string,       // Default: "MXN"
  image_url: string | null,
  available: integer,     // 1 = disponible, 0 = no disponible
  last_updated: datetime,
  created_at: datetime,
  store: Store
}
```

### Store

```typescript
{
  id: integer,
  name: string,
  url: string,
  created_at: datetime
}
```

---

## HTTP Status Codes

| Código | Descripción | Cuándo ocurre |
|--------|-------------|---------------|
| 200 | OK | Request exitoso |
| 404 | Not Found | Recurso no existe |
| 422 | Validation Error | Parámetros inválidos |
| 500 | Internal Server Error | Error del servidor |

---

## OpenAPI Specification

La especificación completa OpenAPI 3.0 está disponible en:

```
GET /openapi.json
```

Puedes importarla en Postman, Insomnia, o cualquier cliente de API.

---

## Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

**Versión:** 0.1.0
**Última actualización:** 6 de diciembre de 2024
