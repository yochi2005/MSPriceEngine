# MSPriceEngine - Explicación Técnica Completa

## 1. Conceptos Importantes del Proyecto

### FastAPI
**¿Qué es?** Framework web moderno para Python que permite crear APIs REST de alto rendimiento.

**¿Por qué lo usamos?**
- Documentación automática (Swagger UI)
- Validación automática de datos
- Soporte nativo para async/await
- Alto rendimiento (comparable a Node.js)

**Ejemplo en nuestro proyecto:**
```python
# En app/main.py
@app.get("/search", response_model=schemas.ProductSearchResponse)
def search_products(
    q: str = Query(..., min_length=2, description="Search query"),
    db: Session = Depends(get_db)
):
    # FastAPI valida automáticamente que 'q' tenga mínimo 2 caracteres
    # Inyecta automáticamente la sesión de base de datos
    products = db.query(models.Product).filter(models.Product.name.ilike(f"%{q}%")).all()
    return {"total": len(products), "products": products}
```

### Pydantic
**¿Qué es?** Librería para validación de datos y serialización usando type hints de Python.

**¿Por qué lo usamos?**
- Valida automáticamente los datos de entrada/salida
- Convierte datos entre formatos (JSON ↔ objetos Python)
- Genera esquemas JSON automáticamente para la documentación

**Ejemplo en nuestro proyecto:**
```python
# En app/schemas.py
class Product(BaseModel):
    id: int                    # Debe ser entero
    name: str                  # Debe ser string
    price: float               # Debe ser float
    store: Store               # Debe ser objeto Store

    class Config:
        from_attributes = True  # Permite convertir desde objetos SQLAlchemy
```

Cuando haces `GET /products/1`, Pydantic automáticamente:
1. Valida que el ID sea un número
2. Convierte el objeto SQLAlchemy a JSON
3. Verifica que todos los campos requeridos existan

### SQLAlchemy
**¿Qué es?** ORM (Object-Relational Mapper) que permite trabajar con bases de datos usando objetos Python en lugar de SQL puro.

**¿Por qué lo usamos?**
- Escribes Python en lugar de SQL
- Cambia fácilmente entre SQLite y PostgreSQL
- Previene SQL injection automáticamente
- Maneja relaciones entre tablas

**Ejemplo en nuestro proyecto:**
```python
# En app/models.py - Definir tabla
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    store = relationship("Store")  # Relación con tabla Store

# En app/main.py - Usar el modelo
# SQL tradicional:
# SELECT * FROM products WHERE name LIKE '%iphone%' LIMIT 50

# SQLAlchemy (lo que usamos):
products = db.query(Product).filter(Product.name.ilike('%iphone%')).limit(50).all()
```

### Scraping Modular
**¿Qué es?** Arquitectura donde cada tienda tiene su propio módulo de scraping independiente.

**Ventajas:**
- Si Amazon cambia su estructura, solo modificas `amazon.py`
- Fácil añadir nuevas tiendas (crear nuevo archivo, heredar de `BaseScraper`)
- Cada scraper tiene su propia lógica sin afectar a otros

**Estructura:**
```
app/scrapers/
├── base.py       ← Clase base con métodos comunes (fetch, clean_price, etc.)
├── amazon.py     ← Hereda de BaseScraper, implementa lógica de Amazon
├── walmart.py    ← Hereda de BaseScraper, implementa lógica de Walmart
└── liverpool.py  ← Hereda de BaseScraper, implementa lógica de Liverpool
```

### Scheduler (APScheduler)
**¿Qué es?** Sistema que ejecuta tareas automáticamente en horarios programados (como cron en Linux).

**¿Por qué lo usamos?**
- Actualiza precios automáticamente cada día
- No necesitas ejecutar scripts manualmente
- Corre en background mientras la API está activa

**Ejemplo en nuestro proyecto:**
```python
# En app/scheduler.py
scheduler.add_job(
    self.run_daily_scrape,           # Función a ejecutar
    trigger=CronTrigger(hour=3),     # Todos los días a las 3:00 AM
    id='daily_scrape'
)
```

### Docker y Docker Compose
**¿Qué es?**
- **Docker**: Empaqueta tu aplicación con todas sus dependencias en un "contenedor"
- **Docker Compose**: Orquesta múltiples contenedores (app, base de datos, etc.)

**¿Por qué lo usamos?**
- "Funciona en mi máquina" → Funciona en todas las máquinas
- Instalación en un comando: `docker-compose up`
- Mismo ambiente en desarrollo y producción

**Nuestro setup:**
```yaml
# docker-compose.yml
services:
  api:                           # Contenedor de la aplicación
    build: .                     # Usa el Dockerfile
    ports:
      - "8000:8000"              # Expone puerto 8000
    volumes:
      - ./data:/app/data         # Persistencia de SQLite
```

---

## 2. Arquitectura General

### Diagrama Mental del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO / CLIENTE                         │
│              (navegador, curl, Postman, etc.)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Request
                         │ GET /search?q=laptop
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     app/main.py                              │
│                   (FastAPI Application)                      │
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │  @app.get("/search")                             │      │
│  │  def search_products(q: str, db: Session):       │      │
│  │      1. Valida parámetros (Pydantic)             │      │
│  │      2. Consulta base de datos (SQLAlchemy)      │      │
│  │      3. Serializa respuesta (Pydantic)           │      │
│  │      4. Retorna JSON                             │      │
│  └──────────────────────────────────────────────────┘      │
└────────┬────────────────────────────┬────────────────────────┘
         │                            │
         │ Dependency Injection       │
         │ get_db()                   │
         ▼                            │
┌─────────────────────┐               │
│  app/database.py    │               │
│                     │               │
│  SessionLocal()     │               │
│  → Conexión DB      │               │
└──────┬──────────────┘               │
       │                              │
       ▼                              │
┌─────────────────────┐               │
│  SQLite/PostgreSQL  │               │
│                     │               │
│  ┌──────────────┐   │               │
│  │ stores       │   │               │
│  │ products     │   │               │
│  └──────────────┘   │               │
│                     │               │
│  Modelos definidos  │               │
│  en app/models.py   │               │
└─────────────────────┘               │
                                      │
                                      │
         ┌────────────────────────────┘
         │ En background (opcional)
         ▼
┌─────────────────────────────────────────────────────────────┐
│                   app/scheduler.py                           │
│                  (APScheduler - Cron Jobs)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │  run_daily_scrape() ejecuta cada día a las 3 AM  │      │
│  │      ↓                                            │      │
│  │  1. Llama a scrapers                             │      │
│  │  2. Obtiene productos                            │      │
│  │  3. Guarda en base de datos                      │      │
│  └──────────────────────────────────────────────────┘      │
└────────┬────────────────────────────────────────────────────┘
         │
         │ Invoca scrapers
         ▼
┌─────────────────────────────────────────────────────────────┐
│                  app/scrapers/                               │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  amazon.py   │  │  walmart.py  │  │ liverpool.py │      │
│  │              │  │              │  │              │      │
│  │  Hereda de   │  │  Hereda de   │  │  Hereda de   │      │
│  │  BaseScraper │  │  BaseScraper │  │  BaseScraper │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │              │
│         └─────────────────┴─────────────────┘              │
│                           │                                │
│                  ┌────────▼────────┐                       │
│                  │   base.py       │                       │
│                  │  (BaseScraper)  │                       │
│                  │                 │                       │
│                  │  - fetch()      │                       │
│                  │  - parse_html() │                       │
│                  │  - clean_price()│                       │
│                  └─────────────────┘                       │
└────────┬────────────────────────────────────────────────────┘
         │
         │ HTTP Requests
         ▼
┌─────────────────────────────────────────────────────────────┐
│              TIENDAS ONLINE (Internet)                       │
│                                                              │
│     amazon.com.mx    walmart.com.mx    liverpool.com.mx     │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de una Petición: GET /search?q=laptop

**Paso a paso:**

```
1. Usuario hace request:
   GET http://localhost:8000/search?q=laptop&min_price=5000

2. FastAPI recibe el request en app/main.py:
   ├─ Endpoint: @app.get("/search")
   ├─ Valida parámetros con Pydantic:
   │  ├─ q: "laptop" ✓
   │  ├─ min_price: 5000 ✓
   │  └─ Query params válidos
   └─ Ejecuta función search_products()

3. Dependency Injection - get_db():
   ├─ app/database.py::get_db() se ejecuta automáticamente
   ├─ Crea SessionLocal() → conexión a SQLite
   └─ Inyecta 'db' como parámetro

4. Query a Base de Datos (SQLAlchemy):
   query = db.query(models.Product)\
       .filter(models.Product.name.ilike('%laptop%'))\
       .filter(models.Product.price >= 5000)\
       .all()

   SQL equivalente:
   SELECT * FROM products
   WHERE name LIKE '%laptop%'
   AND price >= 5000

5. Resultado de la BD:
   [
       Product(id=1, name="Laptop HP", price=8999, store_id=1),
       Product(id=5, name="Laptop Dell", price=12000, store_id=1),
       ...
   ]

6. Serialización (Pydantic):
   ├─ Convierte objetos Product a diccionarios
   ├─ Incluye relación Store (join automático)
   └─ Valida que cumpla schema ProductSearchResponse

7. FastAPI retorna JSON:
   {
       "total": 15,
       "products": [
           {
               "id": 1,
               "name": "Laptop HP 15-dy2021la",
               "price": 8999.0,
               "store": {
                   "id": 1,
                   "name": "Amazon MX",
                   "url": "https://amazon.com.mx"
               },
               "store_url": "https://amazon.com.mx/dp/B08N5XYZ...",
               ...
           },
           ...
       ]
   }

8. Usuario recibe respuesta HTTP 200 con JSON
```

---

## 3. Explicación del Código Importante

### app/main.py (Endpoints de la API)

Este es el **corazón de la aplicación** - define todos los endpoints de la API.

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db, init_db

# Crear aplicación FastAPI
app = FastAPI(
    title="MSPriceEngine API",
    description="Price Search Engine for Mexico",
    version="0.1.0"
)

# Evento de inicio - se ejecuta al levantar la app
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()  # Crea las tablas si no existen
```

**Endpoint principal - Búsqueda de productos:**

```python
@app.get("/search", response_model=schemas.ProductSearchResponse)
def search_products(
    # Parámetros de query - FastAPI los extrae automáticamente
    q: str = Query(..., min_length=2, description="Search query"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    limit: int = Query(50, le=100, description="Number of results"),
    offset: int = Query(0, description="Offset for pagination"),
    # Dependency injection - FastAPI ejecuta get_db() y pasa el resultado
    db: Session = Depends(get_db)
):
    """
    Busca productos por nombre con filtros opcionales.

    Ejemplo: GET /search?q=iphone&min_price=5000&max_price=20000&limit=10
    """

    # Construir query base
    query = db.query(models.Product).filter(
        models.Product.name.ilike(f"%{q}%")  # LIKE case-insensitive
    )

    # Aplicar filtros opcionales
    if store_id:
        query = query.filter(models.Product.store_id == store_id)
    if min_price:
        query = query.filter(models.Product.price >= min_price)
    if max_price:
        query = query.filter(models.Product.price <= max_price)

    # Contar total (antes de paginación)
    total = query.count()

    # Aplicar paginación y ordenar por precio
    products = query.order_by(models.Product.price)\
                    .offset(offset)\
                    .limit(limit)\
                    .all()

    # Pydantic automáticamente serializa esto a JSON
    return schemas.ProductSearchResponse(total=total, products=products)
```

**Otros endpoints importantes:**

```python
# Obtener producto específico
@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Listar todas las tiendas
@app.get("/stores", response_model=list[schemas.Store])
def get_stores(db: Session = Depends(get_db)):
    stores = db.query(models.Store).all()
    return stores

# Health check (para monitoreo)
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

---

### app/models.py (Modelos de Base de Datos)

Define la **estructura de las tablas** usando SQLAlchemy ORM.

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Modelo Store - representa tiendas online
class Store(Base):
    __tablename__ = "stores"  # Nombre de la tabla en la BD

    # Columnas
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # "Amazon MX", "Walmart MX"
    url = Column(String, nullable=False)                 # "https://amazon.com.mx"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación uno-a-muchos: Una tienda tiene muchos productos
    products = relationship("Product", back_populates="store")

    def __repr__(self):
        return f"<Store(name='{self.name}')>"


# Modelo Product - representa productos scrapeados
class Product(Base):
    __tablename__ = "products"

    # Columnas principales
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)  # Indexado para búsquedas rápidas

    # Foreign key - relación con Store
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)

    # Información del producto
    store_url = Column(String, nullable=False)  # URL específica del producto
    sku = Column(String, index=True)            # SKU/ASIN de la tienda (indexado)
    price = Column(Float, nullable=False)
    currency = Column(String, default="MXN")
    image_url = Column(String)
    available = Column(Integer, default=1)      # 1=disponible, 0=agotado

    # Timestamps
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación inversa: Producto pertenece a una tienda
    store = relationship("Store", back_populates="products")

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"
```

**¿Cómo se traducen estos modelos a SQL?**

Cuando ejecutas `init_db()`, SQLAlchemy genera automáticamente:

```sql
-- Tabla stores
CREATE TABLE stores (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    url VARCHAR NOT NULL,
    created_at DATETIME
);

-- Tabla products
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    store_id INTEGER NOT NULL,
    store_url VARCHAR NOT NULL,
    sku VARCHAR,
    price FLOAT NOT NULL,
    currency VARCHAR DEFAULT 'MXN',
    image_url VARCHAR,
    available INTEGER DEFAULT 1,
    last_updated DATETIME,
    created_at DATETIME,
    FOREIGN KEY (store_id) REFERENCES stores(id)
);

-- Índices para búsquedas rápidas
CREATE INDEX idx_product_name ON products(name);
CREATE INDEX idx_product_sku ON products(sku);
```

**Relaciones explicadas:**

```python
# En código Python, puedes navegar fácilmente entre relaciones:

# Obtener tienda de un producto
product = db.query(Product).first()
print(product.store.name)  # "Amazon MX" - SQLAlchemy hace JOIN automático

# Obtener todos los productos de una tienda
store = db.query(Store).first()
for product in store.products:  # SQLAlchemy hace SELECT WHERE store_id = ...
    print(product.name, product.price)
```

---

### app/schemas.py (Validación Request/Response)

Define **esquemas Pydantic** para validar datos de entrada y serializar salida.

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema base para Store (campos comunes)
class StoreBase(BaseModel):
    name: str
    url: str

# Schema para crear una tienda (heredado de StoreBase)
class StoreCreate(StoreBase):
    pass  # Mismo que StoreBase

# Schema para respuesta (incluye campos generados por BD)
class Store(StoreBase):
    id: int              # La BD genera este campo
    created_at: datetime # La BD genera este campo

    class Config:
        from_attributes = True  # Permite convertir desde objetos SQLAlchemy
```

**¿Qué hace `from_attributes = True`?**

```python
# Sin from_attributes = True:
store_dict = {"id": 1, "name": "Amazon MX", "url": "https://..."}
store_schema = Store(**store_dict)  # Funciona

# Con from_attributes = True:
store_obj = db.query(models.Store).first()  # Objeto SQLAlchemy
store_schema = Store.from_orm(store_obj)    # Funciona! Convierte ORM → Pydantic
```

**Schema de Producto (más complejo):**

```python
class ProductBase(BaseModel):
    name: str
    store_id: int
    store_url: str
    sku: Optional[str] = None       # Opcional
    price: float
    currency: str = "MXN"           # Valor por defecto
    image_url: Optional[str] = None
    available: int = 1

class ProductCreate(ProductBase):
    """Schema para crear producto (usado en scrapers)"""
    pass

class Product(ProductBase):
    """Schema para respuesta de API"""
    id: int
    last_updated: datetime
    created_at: datetime
    store: Store  # ← Incluye objeto Store completo (relación)

    class Config:
        from_attributes = True
```

**Ejemplo real de validación:**

```python
# Request inválido: precio como string
data = {
    "name": "iPhone 14",
    "store_id": 1,
    "store_url": "https://...",
    "price": "no es un número"  # ← ERROR
}

try:
    product = ProductCreate(**data)
except ValidationError as e:
    print(e.json())
    # {
    #   "price": ["value is not a valid float"]
    # }

# Request válido
data["price"] = 15999.99
product = ProductCreate(**data)  # ✓ OK
```

**Schema de respuesta de búsqueda:**

```python
class ProductSearchResponse(BaseModel):
    """Response para endpoint /search"""
    total: int              # Total de resultados (sin paginación)
    products: list[Product] # Lista de productos (con paginación)

# Uso en endpoint:
return ProductSearchResponse(
    total=150,           # Se encontraron 150 productos
    products=products[:50]  # Pero solo devolvemos 50 (página 1)
)
```

---

### app/scrapers/base.py (Clase Base para Scrapers)

Define la **clase base** que todos los scrapers heredan.

```python
import httpx
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import logging
import asyncio

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Clase base para todos los scrapers de tiendas."""

    def __init__(self, store_name: str, base_url: str):
        self.store_name = store_name  # "Amazon MX"
        self.base_url = base_url      # "https://amazon.com.mx"

        # Headers para simular navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
            'Accept': 'text/html,application/xhtml+xml,...',
            'Accept-Language': 'es-MX,es;q=0.9',
            'DNT': '1',  # Do Not Track
        }

    async def fetch(self, url: str, retry: int = 3) -> Optional[str]:
        """
        Hace HTTP request y retorna HTML.
        Incluye reintentos con backoff exponencial.
        """
        for attempt in range(retry):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(url, headers=self.headers)
                    response.raise_for_status()  # Lanza excepción si 4xx/5xx
                    logger.info(f"Successfully fetched {url}")
                    return response.text
            except httpx.HTTPError as e:
                logger.warning(f"Attempt {attempt + 1}/{retry} failed: {e}")
                if attempt < retry - 1:
                    await asyncio.sleep(2 ** attempt)  # Espera: 1s, 2s, 4s
                else:
                    logger.error(f"Failed after {retry} attempts")
                    return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parsea HTML con BeautifulSoup."""
        return BeautifulSoup(html, 'lxml')

    def clean_price(self, price_text: str) -> Optional[float]:
        """
        Limpia texto de precio y convierte a float.

        Ejemplos:
            "$1,299.99"     → 1299.99
            "$ 1299"        → 1299.0
            "MXN 1,299.99"  → 1299.99
        """
        try:
            # Remover símbolos, comas, espacios
            cleaned = price_text.replace('$', '')\
                                .replace(',', '')\
                                .replace(' ', '')\
                                .replace('MXN', '')\
                                .strip()
            return float(cleaned)
        except (ValueError, AttributeError):
            logger.warning(f"Failed to parse price: {price_text}")
            return None

    def clean_name(self, name: str) -> str:
        """Limpia nombre de producto (remueve espacios extra)."""
        return ' '.join(name.split()).strip()

    # Métodos abstractos - DEBEN ser implementados por cada scraper
    @abstractmethod
    async def scrape_search(self, query: str, max_results: int = 20) -> List[Dict]:
        """Scrapea resultados de búsqueda."""
        pass

    @abstractmethod
    async def scrape_product(self, url: str) -> Optional[Dict]:
        """Scrapea página de producto individual."""
        pass
```

**¿Por qué usar clase abstracta (ABC)?**

```python
# Intento crear instancia de BaseScraper directamente
scraper = BaseScraper("Test", "https://test.com")
# ERROR: Can't instantiate abstract class BaseScraper

# Debo crear subclase que implemente los métodos abstractos
class MiScraper(BaseScraper):
    async def scrape_search(self, query, max_results=20):
        # Implementación aquí
        pass

    async def scrape_product(self, url):
        # Implementación aquí
        pass

scraper = MiScraper("Mi Tienda", "https://...")  # ✓ OK
```

---

### app/scrapers/amazon.py (Implementación de Scraper)

Implementa scraping específico para Amazon México.

```python
from typing import List, Dict, Optional
from urllib.parse import quote_plus
from .base import BaseScraper

class AmazonScraper(BaseScraper):
    """Scraper para Amazon Mexico."""

    def __init__(self):
        # Llama al constructor de BaseScraper
        super().__init__(
            store_name="Amazon MX",
            base_url="https://www.amazon.com.mx"
        )

    async def scrape_search(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Scrapea página de búsqueda de Amazon.

        Args:
            query: "laptop gaming"
            max_results: 20

        Returns:
            [
                {
                    "name": "Laptop HP Pavilion Gaming...",
                    "price": 12999.99,
                    "url": "https://amazon.com.mx/dp/B08XYZ...",
                    "sku": "B08XYZ123",
                    "image_url": "https://...",
                    "available": True
                },
                ...
            ]
        """
        # Construir URL de búsqueda
        # "laptop gaming" → "laptop+gaming"
        search_url = f"{self.base_url}/s?k={quote_plus(query)}"
        # Resultado: https://amazon.com.mx/s?k=laptop+gaming

        logger.info(f"Scraping Amazon MX search: {search_url}")

        # Fetch HTML (usa método heredado de BaseScraper)
        html = await self.fetch(search_url)
        if not html:
            return []

        # Parsear HTML
        soup = self.parse_html(html)
        products = []

        # Amazon usa div con atributo data-component-type="s-search-result"
        result_items = soup.find_all(
            'div',
            {'data-component-type': 's-search-result'},
            limit=max_results
        )

        # Procesar cada resultado
        for item in result_items:
            try:
                product = self._parse_search_item(item)
                if product:  # Solo añadir si parsing fue exitoso
                    products.append(product)
            except Exception as e:
                logger.warning(f"Failed to parse item: {e}")
                continue  # Saltar este item, continuar con siguiente

        logger.info(f"Found {len(products)} products on Amazon MX")
        return products

    def _parse_search_item(self, item) -> Optional[Dict]:
        """
        Parsea un elemento de resultado de búsqueda.

        HTML de Amazon (simplificado):
        <div data-component-type="s-search-result" data-asin="B08XYZ123">
            <h2 class="s-line-clamp-2">
                <a href="/dp/B08XYZ123">Laptop HP Pavilion...</a>
            </h2>
            <span class="a-price-whole">12,999</span>
            <span class="a-price-fraction">99</span>
            <img class="s-image" src="https://...">
        </div>
        """
        try:
            # 1. Nombre del producto
            name_elem = item.find('h2', class_='s-line-clamp-2')
            if not name_elem:
                return None  # Sin nombre = item inválido
            name = self.clean_name(name_elem.get_text())

            # 2. URL del producto
            link_elem = item.find('a', class_='a-link-normal s-no-outline')
            if not link_elem or not link_elem.get('href'):
                return None
            # href puede ser "/dp/B08XYZ?ref=..." - remover query params
            url = self.base_url + link_elem['href'].split('?')[0]

            # 3. Precio (Amazon tiene formato especial)
            price = None
            price_whole = item.find('span', class_='a-price-whole')
            price_fraction = item.find('span', class_='a-price-fraction')

            if price_whole:
                # "12,999" + "99" = "12,999.99"
                price_text = price_whole.get_text() + \
                             (price_fraction.get_text() if price_fraction else '00')
                price = self.clean_price(price_text)  # Método heredado

            if not price:
                return None  # Sin precio = no tiene sentido guardar

            # 4. Imagen
            image_elem = item.find('img', class_='s-image')
            image_url = image_elem.get('src') if image_elem else None

            # 5. SKU (ASIN de Amazon)
            asin = item.get('data-asin')

            return {
                'name': name,
                'price': price,
                'url': url,
                'sku': asin,
                'image_url': image_url,
                'available': True  # Si está en resultados, está disponible
            }

        except Exception as e:
            logger.warning(f"Error parsing Amazon item: {e}")
            return None

    async def scrape_product(self, url: str) -> Optional[Dict]:
        """
        Scrapea página individual de producto.
        Similar a scrape_search pero con más detalles.
        """
        # Implementación similar pero parseando página de detalle
        # ...
        pass
```

**Flujo completo de scraping:**

```python
# 1. Instanciar scraper
scraper = AmazonScraper()

# 2. Scrape search results
import asyncio
products = asyncio.run(scraper.scrape_search("laptop", max_results=10))

# 3. Resultado:
[
    {
        "name": "Laptop HP Pavilion Gaming 15-dk1036la",
        "price": 12999.99,
        "url": "https://amazon.com.mx/dp/B08N5XQWB7",
        "sku": "B08N5XQWB7",
        "image_url": "https://m.media-amazon.com/images/I/...",
        "available": True
    },
    # ... 9 más
]

# 4. Guardar en base de datos (ver scheduler.py)
```

---

### app/database.py (Conexión a Base de Datos)

Maneja la **configuración y conexión** a la base de datos.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Leer URL de base de datos desde variable de entorno
# Por defecto: SQLite en ./data/price_search.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/price_search.db")

# Crear engine (conexión a BD)
engine = create_engine(
    DATABASE_URL,
    # SQLite requiere check_same_thread=False para FastAPI
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Session factory - crea nuevas sesiones de BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class - todos los modelos heredan de aquí
Base = declarative_base()

def get_db():
    """
    Dependency para FastAPI - provee sesión de BD.
    Se ejecuta automáticamente en cada request.
    """
    db = SessionLocal()  # Crear nueva sesión
    try:
        yield db  # Proveer sesión al endpoint
    finally:
        db.close()  # Cerrar sesión al terminar request

def init_db():
    """
    Inicializa base de datos - crea todas las tablas.
    Se ejecuta al startup de la aplicación.
    """
    Base.metadata.create_all(bind=engine)
```

**¿Cómo funciona `get_db()` con Dependency Injection?**

```python
# En app/main.py
@app.get("/search")
def search_products(
    q: str,
    db: Session = Depends(get_db)  # ← FastAPI ejecuta get_db()
):
    # db es una sesión activa de SQLAlchemy
    products = db.query(Product).all()
    # ...
    # Cuando termina la función, FastAPI ejecuta db.close() automáticamente
```

**Flujo visual:**

```
Request llega
    ↓
FastAPI ve: db: Session = Depends(get_db)
    ↓
Ejecuta get_db():
    db = SessionLocal()  ← Abre conexión
    yield db             ← Pausa aquí, pasa db al endpoint
    ↓
Endpoint se ejecuta con db
    ↓
Endpoint termina (return)
    ↓
FastAPI reanuda get_db():
    db.close()           ← Cierra conexión
    ↓
Response enviado
```

**Cambiar de SQLite a PostgreSQL:**

```python
# .env file
# Antes (SQLite):
DATABASE_URL=sqlite:///./data/price_search.db

# Después (PostgreSQL):
DATABASE_URL=postgresql://user:password@localhost:5432/priceengine

# No necesitas cambiar código - SQLAlchemy maneja la diferencia
```

---

## 4. Cómo Funciona el Scraping

### Flujo Completo de Scraping para Amazon

```
1. Scheduler dispara job (3:00 AM):
   scheduler.run_daily_scrape()

2. Scheduler llama a scraper:
   scraper = AmazonScraper()
   products = await scraper.scrape_search("laptop", max_results=20)

3. scrape_search() construye URL:
   https://amazon.com.mx/s?k=laptop

4. fetch() hace HTTP request:
   ├─ Usa headers de navegador real
   ├─ Timeout de 30 segundos
   ├─ Reintentos automáticos si falla
   └─ Retorna HTML completo

5. parse_html() procesa HTML:
   soup = BeautifulSoup(html, 'lxml')

6. Encuentra elementos de productos:
   items = soup.find_all('div', {'data-component-type': 's-search-result'})

7. Para cada item:
   ├─ Extrae nombre: <h2 class="s-line-clamp-2">...</h2>
   ├─ Extrae precio: <span class="a-price-whole">...</span>
   ├─ Extrae URL: <a href="/dp/...">
   ├─ Extrae imagen: <img class="s-image" src="...">
   └─ Extrae ASIN: data-asin="B08XYZ123"

8. Limpia datos:
   ├─ clean_price("$12,999.99") → 12999.99
   └─ clean_name("  Laptop HP  ") → "Laptop HP"

9. Retorna lista de diccionarios:
   [
       {"name": "...", "price": 12999.99, ...},
       {"name": "...", "price": 8500.00, ...},
       ...
   ]

10. Scheduler guarda en BD:
    for product_data in products:
        # Verificar si existe (por SKU)
        existing = db.query(Product).filter(
            Product.sku == product_data['sku'],
            Product.store_id == store.id
        ).first()

        if existing:
            # Actualizar precio
            existing.price = product_data['price']
            existing.last_updated = datetime.utcnow()
        else:
            # Crear nuevo producto
            new_product = Product(**product_data, store_id=store.id)
            db.add(new_product)

        db.commit()
```

### Cómo Agregar una Nueva Tienda

**Paso 1: Crear archivo del scraper**

```bash
touch app/scrapers/coppel.py
```

**Paso 2: Implementar clase heredando de BaseScraper**

```python
# app/scrapers/coppel.py
from typing import List, Dict, Optional
from urllib.parse import quote_plus
from .base import BaseScraper
import logging

logger = logging.getLogger(__name__)

class CoppelScraper(BaseScraper):
    """Scraper para Coppel México."""

    def __init__(self):
        super().__init__(
            store_name="Coppel",
            base_url="https://www.coppel.com"
        )

    async def scrape_search(self, query: str, max_results: int = 20) -> List[Dict]:
        """Implementa búsqueda en Coppel."""
        # 1. Construir URL de búsqueda de Coppel
        search_url = f"{self.base_url}/search?q={quote_plus(query)}"

        # 2. Fetch HTML
        html = await self.fetch(search_url)
        if not html:
            return []

        # 3. Parsear (inspeccionar estructura HTML de Coppel primero)
        soup = self.parse_html(html)
        products = []

        # TODO: Inspeccionar Coppel.com y encontrar selectores CSS correctos
        # Ejemplo genérico:
        items = soup.find_all('div', class_='product-item', limit=max_results)

        for item in items:
            try:
                name = item.find('h3', class_='product-name').get_text()
                price_text = item.find('span', class_='price').get_text()
                price = self.clean_price(price_text)
                url = self.base_url + item.find('a')['href']

                products.append({
                    'name': self.clean_name(name),
                    'price': price,
                    'url': url,
                    'sku': None,  # Si Coppel no expone SKU
                    'image_url': item.find('img')['src'] if item.find('img') else None,
                    'available': True
                })
            except Exception as e:
                logger.warning(f"Error parsing Coppel item: {e}")
                continue

        return products

    async def scrape_product(self, url: str) -> Optional[Dict]:
        """Implementa scraping de página individual."""
        # Similar a scrape_search pero para una URL específica
        pass
```

**Paso 3: Registrar en __init__.py**

```python
# app/scrapers/__init__.py
from .base import BaseScraper
from .amazon import AmazonScraper
from .walmart import WalmartScraper
from .liverpool import LiverpoolScraper
from .coppel import CoppelScraper  # ← Añadir

__all__ = [
    "BaseScraper",
    "AmazonScraper",
    "WalmartScraper",
    "LiverpoolScraper",
    "CoppelScraper"  # ← Añadir
]
```

**Paso 4: Añadir al scheduler**

```python
# app/scheduler.py
class ScraperScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scrapers = {
            'amazon': AmazonScraper(),
            'walmart': WalmartScraper(),
            'liverpool': LiverpoolScraper(),
            'coppel': CoppelScraper()  # ← Añadir
        }
```

**Paso 5: Habilitar en run_daily_scrape()**

```python
# app/scheduler.py - método run_daily_scrape()
loop.run_until_complete(self.scrape_store('amazon', queries))
loop.run_until_complete(self.scrape_store('coppel', queries))  # ← Añadir
```

### Buenas Prácticas para Scrapers

**1. Respetar rate limiting**
```python
import asyncio

async def scrape_multiple_pages(self, pages: int):
    for page in range(pages):
        await self.fetch(f"{self.base_url}/search?page={page}")
        await asyncio.sleep(2)  # Esperar 2 segundos entre requests
```

**2. Usar selectores robustos**
```python
# Malo - muy específico, se rompe fácil
price = soup.find('div', class_='price-box-wrapper-v2-mobile')

# Bueno - múltiples fallbacks
price = (
    soup.find('span', {'data-testid': 'price'}) or
    soup.find('span', class_='price') or
    soup.find('div', class_='product-price')
)
```

**3. Logging detallado**
```python
logger.info(f"Scraping {self.store_name} - query: {query}")
logger.debug(f"Found {len(items)} items in HTML")
logger.warning(f"Failed to parse item {i}: missing price")
logger.error(f"HTTP error {response.status_code} for {url}")
```

**4. Manejo de errores granular**
```python
def _parse_search_item(self, item):
    try:
        name = item.find('h2').get_text()
    except AttributeError:
        logger.warning("Item missing name element")
        return None

    try:
        price = self.clean_price(item.find('span', class_='price').get_text())
    except (AttributeError, ValueError):
        logger.warning(f"Item '{name}' has invalid price")
        return None

    # Continue parsing...
```

**5. Headers realistas**
```python
self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
    'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': self.base_url,  # Simular que venimos del sitio
    'DNT': '1',
}
```

**6. Inspeccionar antes de implementar**
```bash
# 1. Abrir Chrome DevTools (F12)
# 2. Ir a Network tab
# 3. Hacer búsqueda en la tienda
# 4. Ver si hay API calls en lugar de HTML
# 5. Si hay API, es más fácil parsear JSON que HTML

# Ejemplo: Walmart MX usa API GraphQL
# En vez de parsear HTML:
POST https://www.walmart.com.mx/api/graphql
{
    "query": "search",
    "variables": {"query": "laptop"}
}

# Respuesta: JSON fácil de parsear
{
    "data": {
        "products": [
            {"name": "...", "price": 12999, ...}
        ]
    }
}
```

---

## 5. Próximas Mejoras Recomendadas

### 1. Implementar Scrapers de Walmart y Liverpool

**Walmart MX - Requiere JavaScript rendering**

```python
# Problema: Walmart carga productos con JavaScript
# Solución: Usar Playwright en lugar de httpx

# Instalar Playwright
# pip install playwright
# playwright install chromium

# Modificar WalmartScraper
from playwright.async_api import async_playwright

class WalmartScraper(BaseScraper):
    async def fetch(self, url: str) -> str:
        """Override fetch para usar Playwright."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until='networkidle')
            html = await page.content()
            await browser.close()
            return html
```

**Liverpool - Similar implementación**

```python
# Liverpool también puede requerir JS rendering
# O puede tener API pública - inspeccionar primero

class LiverpoolScraper(BaseScraper):
    async def scrape_search(self, query: str, max_results: int = 20):
        # 1. Inspeccionar Liverpool.com.mx
        # 2. Buscar API calls en Network tab
        # 3. Si hay API, usar directamente
        # 4. Si no, usar Playwright como Walmart
        pass
```

### 2. Migrar de SQLite a PostgreSQL

**Por qué PostgreSQL:**
- SQLite no maneja bien concurrencia (scrapers + API simultáneos)
- PostgreSQL tiene mejor full-text search
- PostgreSQL escala mejor con millones de productos

**Cómo migrar:**

```yaml
# docker-compose.yml - descomentar PostgreSQL
services:
  api:
    environment:
      - DATABASE_URL=postgresql://priceengine:priceengine123@db:5432/priceengine
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=priceengine
      - POSTGRES_PASSWORD=priceengine123
      - POSTGRES_DB=priceengine
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```python
# No cambiar código Python - SQLAlchemy maneja automáticamente

# Opcional: Mejorar búsqueda con full-text search de PostgreSQL
# app/models.py
from sqlalchemy import Index, func

class Product(Base):
    # ... campos existentes ...

    # Añadir índice de full-text search
    __table_args__ = (
        Index('idx_product_search', 'name', postgresql_using='gin',
              postgresql_ops={'name': 'gin_trgm_ops'}),
    )

# app/main.py - mejorar búsqueda
query = db.query(Product).filter(
    func.similarity(Product.name, q) > 0.3  # Búsqueda fuzzy
).order_by(
    func.similarity(Product.name, q).desc()
)
```

### 3. Activar Scheduler y Manejar Tareas Asíncronas

**Actualmente el scheduler está deshabilitado. Para activarlo:**

```python
# app/main.py - añadir startup
from .scheduler import scheduler

@app.on_event("startup")
async def startup_event():
    init_db()
    scheduler.start()  # ← Activar scheduler

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.stop()  # ← Parar scheduler al cerrar
```

**Problema: Scrapers bloquean la API**

```python
# Solución: Usar Celery para tareas en background

# 1. Instalar Celery + Redis
# pip install celery redis

# 2. Crear app/celery_app.py
from celery import Celery

celery_app = Celery(
    'mspriceengine',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def scrape_store_task(store_name: str, queries: list):
    """Ejecuta scraping en background."""
    # ... código de scraping ...
    pass

# 3. Ejecutar worker en terminal separado
# celery -A app.celery_app worker --loglevel=info

# 4. Encolar tarea desde scheduler
from app.celery_app import scrape_store_task
scrape_store_task.delay('amazon', ['laptop', 'iphone'])
```

### 4. Añadir Price History (Historial de Precios)

```python
# app/models.py - nuevo modelo
class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="price_history")

# Modificar Product
class Product(Base):
    # ... campos existentes ...
    price_history = relationship("PriceHistory", back_populates="product")

# app/scheduler.py - guardar histórico al actualizar
if existing:
    # Guardar precio anterior en histórico
    history = PriceHistory(
        product_id=existing.id,
        price=existing.price
    )
    db.add(history)

    # Actualizar precio actual
    existing.price = product_data['price']
    db.commit()

# app/main.py - endpoint de histórico
@app.get("/products/{product_id}/price-history")
def get_price_history(
    product_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    history = db.query(PriceHistory)\
        .filter(PriceHistory.product_id == product_id)\
        .filter(PriceHistory.recorded_at >= datetime.utcnow() - timedelta(days=days))\
        .order_by(PriceHistory.recorded_at)\
        .all()
    return history
```

### 5. Matching de Productos entre Tiendas

```python
# app/utils/matcher.py
from difflib import SequenceMatcher

def calculate_similarity(name1: str, name2: str) -> float:
    """Calcula similitud entre nombres de productos."""
    return SequenceMatcher(None, name1.lower(), name2.lower()).ratio()

def find_matching_products(product: Product, db: Session, threshold: float = 0.8):
    """Encuentra productos similares en otras tiendas."""
    other_products = db.query(Product)\
        .filter(Product.store_id != product.store_id)\
        .all()

    matches = []
    for other in other_products:
        similarity = calculate_similarity(product.name, other.name)
        if similarity >= threshold:
            matches.append({
                'product': other,
                'similarity': similarity
            })

    return sorted(matches, key=lambda x: x['similarity'], reverse=True)

# app/main.py - endpoint de comparación
@app.get("/products/{product_id}/compare")
def compare_prices(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    matches = find_matching_products(product, db)

    return {
        'product': product,
        'alternatives': [
            {
                'store': m['product'].store.name,
                'price': m['product'].price,
                'url': m['product'].store_url,
                'similarity': m['similarity']
            }
            for m in matches[:5]  # Top 5 matches
        ]
    }
```

### 6. Rate Limiting para API

```python
# pip install slowapi

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/search")
@limiter.limit("100/minute")  # 100 requests por minuto por IP
def search_products(request: Request, q: str, db: Session = Depends(get_db)):
    # ... código existente ...
    pass
```

### 7. Tests Completos

```python
# tests/test_scrapers.py
import pytest
from app.scrapers import AmazonScraper

@pytest.mark.asyncio
async def test_amazon_scraper():
    scraper = AmazonScraper()
    products = await scraper.scrape_search("laptop", max_results=5)

    assert len(products) > 0
    assert all('name' in p for p in products)
    assert all('price' in p for p in products)
    assert all(isinstance(p['price'], float) for p in products)

# tests/test_price_cleaning.py
def test_clean_price():
    from app.scrapers.base import BaseScraper

    scraper = BaseScraper("Test", "https://test.com")

    assert scraper.clean_price("$1,299.99") == 1299.99
    assert scraper.clean_price("$ 1299") == 1299.0
    assert scraper.clean_price("MXN 1,299.99") == 1299.99
    assert scraper.clean_price("invalid") is None
```

---

## Resumen Final

### Flujo Completo del Sistema

```
1. Usuario → GET /search?q=laptop
2. FastAPI valida parámetros (Pydantic)
3. Dependency injection provee sesión DB
4. SQLAlchemy query a base de datos
5. Pydantic serializa resultados
6. FastAPI retorna JSON

En background (scheduler):
1. APScheduler dispara job diario
2. Scrapers (Amazon, Walmart, Liverpool) scrapean tiendas
3. BeautifulSoup parsea HTML
4. SQLAlchemy guarda/actualiza productos
5. Sistema listo para consultas actualizadas
```

### Archivos Clave y Responsabilidades

| Archivo | Responsabilidad |
|---------|----------------|
| main.py | Endpoints de API, routing, validación |
| models.py | Esquema de base de datos (tablas) |
| schemas.py | Validación request/response (Pydantic) |
| database.py | Conexión a BD, sessions |
| scheduler.py | Jobs automáticos, orchestration de scrapers |
| scrapers/base.py | Lógica común de scraping |
| scrapers/amazon.py | Scraping específico de Amazon MX |
| scrapers/walmart.py | Scraping específico de Walmart MX (TODO) |
| scrapers/liverpool.py | Scraping específico de Liverpool (TODO) |

### Tecnologías y Su Rol

- FastAPI: Framework web, genera API REST automáticamente
- Pydantic: Validación de datos, serialización JSON
- SQLAlchemy: ORM, abstracción de base de datos
- BeautifulSoup: Parsing de HTML
- httpx: HTTP client asíncrono
- APScheduler: Scheduler para tareas periódicas
- Docker: Containerización, portabilidad
