# Estructura del Proyecto - MSPriceEngine

## Diagrama de Directorios

```
MSPriceEngine/
├── 📂 app/                          # Código fuente de la aplicación
│   ├── __init__.py                 # Marca app como paquete Python
│   ├── main.py                     # Aplicación FastAPI principal
│   ├── models.py                   # Modelos de base de datos (SQLAlchemy)
│   ├── schemas.py                  # Esquemas de validación (Pydantic)
│   ├── database.py                 # Configuración de base de datos
│   ├── scheduler.py                # Tareas programadas (APScheduler)
│   └── 📂 scrapers/                # Módulos de web scraping
│       ├── __init__.py
│       ├── base.py                 # Clase base abstracta para scrapers
│       ├── amazon.py               # Scraper específico para Amazon MX
│       ├── walmart.py              # Scraper específico para Walmart MX
│       └── liverpool.py            # Scraper específico para Liverpool
│
├── 📂 data/                         # Datos persistentes
│   └── price_search.db            # Base de datos SQLite (creada automáticamente)
│
├── 📂 docs/                         # Documentación del proyecto
│   ├── ARCHITECTURE.md            # Arquitectura técnica completa
│   ├── API_GUIDE.md               # Guía de uso de la API
│   ├── API_ENDPOINTS.md           # Referencia de endpoints
│   ├── SETUP_GUIDE.md             # Guía de instalación
│   ├── PROJECT_STRUCTURE.md       # Este archivo
│   └── FRONTEND_REQUIREMENTS.md   # Especificaciones del frontend
│
├── 📂 tests/                        # Tests automatizados
│   ├── __init__.py
│   └── test_api.py                # Tests de la API
│
├── 📂 venv/                         # Ambiente virtual de Python (gitignored)
│   ├── bin/                       # Ejecutables (python, pip, activate)
│   ├── lib/                       # Librerías instaladas
│   └── ...
│
├── 📄 requirements.txt              # Dependencias de Python
├── 📄 .env.example                  # Ejemplo de variables de entorno
├── 📄 .gitignore                    # Archivos ignorados por Git
├── 📄 Dockerfile                    # Configuración de Docker
├── 📄 docker-compose.yml            # Orquestación de contenedores
├── 📄 LICENSE                       # Licencia MIT
├── 📄 README.md                     # Documentación principal
├── 📄 test_api_manual.py            # Script de pruebas manuales
├── 📄 RESUMEN_COMPLETO.md           # Resumen ejecutivo
└── 📄 MSPriceEngine_Explanation.txt # Explicación técnica detallada
```

---

## Descripción de Directorios

### `/app` - Aplicación Principal

Contiene todo el código de la API backend.

**Archivos clave:**

| Archivo | Propósito | Líneas aprox. | Complejidad |
|---------|-----------|---------------|-------------|
| `main.py` | Endpoints de FastAPI, routes | ~150 | Media |
| `models.py` | Definición de tablas de BD | ~60 | Baja |
| `schemas.py` | Validación de request/response | ~70 | Baja |
| `database.py` | Conexión y sesiones de BD | ~40 | Baja |
| `scheduler.py` | Jobs programados de scraping | ~120 | Media |

**Responsabilidades:**
- Definir endpoints HTTP
- Validar datos de entrada/salida
- Interactuar con la base de datos
- Orquestar scrapers
- Manejar errores

### `/app/scrapers` - Módulos de Scraping

Cada scraper es independiente y extrae datos de una tienda específica.

**Arquitectura:**
```
BaseScraper (clase abstracta)
    ↓ hereda
AmazonScraper
WalmartScraper
LiverpoolScraper
```

**Responsabilidades:**
- Hacer requests HTTP a tiendas
- Parsear HTML/JavaScript
- Extraer información de productos
- Normalizar datos (precios, nombres)
- Manejar anti-bot measures

### `/data` - Datos Persistentes

Almacena la base de datos SQLite en desarrollo.

**Archivos:**
- `price_search.db` - Base de datos principal
- `price_search.db-journal` - Journal de transacciones (temporal)

**Nota:** En producción se usaría PostgreSQL en servidor externo.

### `/docs` - Documentación

Documentación técnica y guías de usuario.

| Archivo | Audiencia | Propósito |
|---------|-----------|-----------|
| `ARCHITECTURE.md` | Desarrolladores | Arquitectura técnica completa |
| `API_GUIDE.md` | Usuarios de API | Cómo usar los endpoints |
| `API_ENDPOINTS.md` | Desarrolladores | Referencia rápida de endpoints |
| `SETUP_GUIDE.md` | Nuevos desarrolladores | Instalación y configuración |
| `PROJECT_STRUCTURE.md` | Desarrolladores | Esta documentación |
| `FRONTEND_REQUIREMENTS.md` | Frontend devs | Specs para crear UI |

### `/tests` - Tests Automatizados

Tests unitarios y de integración.

**Tipos de tests:**
- Tests de endpoints (`test_api.py`)
- Tests de scrapers (futuro)
- Tests de modelos (futuro)
- Tests de integración (futuro)

### `/venv` - Ambiente Virtual

Ambiente aislado de Python con todas las dependencias.

**No se versiona en Git** (incluido en `.gitignore`)

**Estructura:**
```
venv/
├── bin/activate        # Script para activar venv
├── bin/python         # Python del venv
├── bin/pip            # pip del venv
├── lib/python3.13/    # Librerías instaladas
└── ...
```

---

## Archivos de Configuración

### `requirements.txt`

Lista todas las dependencias de Python del proyecto.

**Secciones:**
1. **Web framework** - FastAPI, Uvicorn
2. **Database** - SQLAlchemy, Alembic
3. **Scraping** - httpx, BeautifulSoup4
4. **Utilities** - APScheduler, python-dotenv
5. **Testing** - pytest, pytest-asyncio

**Uso:**
```bash
pip install -r requirements.txt
```

### `.env.example`

Plantilla de variables de entorno.

**Copiar y configurar:**
```bash
cp .env.example .env
# Editar .env con tus valores
```

**Variables importantes:**
- `DATABASE_URL` - Conexión a BD
- `ENABLE_SCHEDULER` - Activar/desactivar scraping automático
- `LOG_LEVEL` - Nivel de logging

### `Dockerfile`

Define cómo construir la imagen Docker de la aplicación.

**Pasos:**
1. Base: Python 3.11-slim
2. Instalar dependencias del sistema
3. Copiar `requirements.txt` e instalar
4. Copiar código fuente
5. Exponer puerto 8000
6. Comando: `uvicorn app.main:app`

### `docker-compose.yml`

Orquesta múltiples contenedores (app + BD en futuro).

**Servicios actuales:**
- `api` - Aplicación FastAPI

**Servicios futuros:**
- `db` - PostgreSQL
- `redis` - Cache
- `frontend` - React app

### `.gitignore`

Define qué archivos NO versionar en Git.

**Ignorados:**
- `venv/` - Ambiente virtual
- `data/` - Base de datos
- `__pycache__/` - Cache de Python
- `.env` - Variables de entorno
- `*.log` - Archivos de log

---

## Flujo de Datos

### Request HTTP → Response

```
1. Usuario hace request
   GET /search?q=laptop

2. FastAPI recibe en main.py
   @app.get("/search")
   def search_products(...)

3. Valida parámetros con Pydantic
   schemas.ProductSearchResponse

4. Consulta BD vía database.py
   db.query(models.Product)

5. Serializa respuesta
   Pydantic convierte objetos → JSON

6. Retorna JSON al usuario
```

### Scraping → Base de Datos

```
1. Scheduler dispara job (scheduler.py)
   run_daily_scrape()

2. Llama a scraper específico
   amazon_scraper.scrape_search("laptop")

3. Scraper hace HTTP request
   base.py::fetch()

4. Parsea HTML
   BeautifulSoup + selectores CSS

5. Extrae datos
   clean_price(), clean_name()

6. Retorna lista de productos
   [{"name": "...", "price": 12999.99}]

7. Scheduler guarda en BD
   db.add(Product(...))
   db.commit()
```

---

## Patrones de Diseño Utilizados

### 1. Strategy Pattern (Scrapers)

Cada tienda tiene su propia estrategia de scraping:

```python
class BaseScraper(ABC):
    @abstractmethod
    async def scrape_search(...):
        pass

class AmazonScraper(BaseScraper):
    async def scrape_search(...):
        # Implementación específica de Amazon

class WalmartScraper(BaseScraper):
    async def scrape_search(...):
        # Implementación específica de Walmart
```

### 2. Dependency Injection (Database)

FastAPI inyecta dependencias automáticamente:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/search")
def search_products(db: Session = Depends(get_db)):
    # db es inyectada automáticamente
    products = db.query(Product).all()
```

### 3. Repository Pattern (Models)

Los modelos SQLAlchemy actúan como repositorios:

```python
class Product(Base):
    __tablename__ = "products"
    # Campos...

# Uso:
db.query(Product).filter(Product.name.ilike('%laptop%')).all()
```

### 4. Factory Pattern (Scrapers)

El scheduler actúa como factory de scrapers:

```python
self.scrapers = {
    'amazon': AmazonScraper(),
    'walmart': WalmartScraper(),
    'liverpool': LiverpoolScraper()
}

scraper = self.scrapers.get(store_name)
```

---

## Convenciones de Código

### Naming

- **Archivos:** `snake_case.py`
- **Clases:** `PascalCase`
- **Funciones/métodos:** `snake_case`
- **Constantes:** `UPPER_CASE`
- **Variables privadas:** `_leading_underscore`

### Imports

```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party
from fastapi import FastAPI
from sqlalchemy import Column

# 3. Local
from . import models
from .database import get_db
```

### Docstrings

```python
def search_products(q: str) -> list:
    """
    Busca productos por nombre.

    Args:
        q: Término de búsqueda

    Returns:
        Lista de productos encontrados
    """
    pass
```

---

## Tamaño del Proyecto

### Líneas de Código

| Componente | Líneas | Archivos |
|-----------|--------|----------|
| app/*.py | ~500 | 5 |
| app/scrapers/*.py | ~400 | 4 |
| tests/*.py | ~100 | 2 |
| docs/*.md | ~2000 | 6 |
| **Total** | **~3000** | **17** |

### Complejidad

- **Baja:** models.py, schemas.py, database.py
- **Media:** main.py, scheduler.py, scrapers/base.py
- **Alta:** scrapers específicos (requieren mantenimiento)

---

## Dependencias entre Módulos

```
main.py
    ├── models.py
    ├── schemas.py
    ├── database.py
    └── (indirectamente) scheduler.py

scheduler.py
    ├── database.py
    ├── models.py
    └── scrapers/*.py

scrapers/*.py
    └── scrapers/base.py

models.py
    └── database.py (Base)

schemas.py
    └── (ninguna - solo Pydantic)
```

**Nota:** No hay dependencias circulares.

---

## Archivos que NO debes Editar

❌ **No tocar:**
- `venv/` - Generado automáticamente
- `data/price_search.db` - Manejado por SQLAlchemy
- `__pycache__/` - Cache de Python
- `.git/` - Control de versiones

❌ **No versionar:**
- `.env` - Contiene secrets
- Archivos de log
- Bases de datos locales

---

## Próximas Adiciones Planeadas

### Nuevos Directorios

```
app/
├── utils/           # Utilidades compartidas
├── middleware/      # Middleware custom
└── api/            # Routes organizadas por versión
    └── v1/
        ├── products.py
        └── stores.py

migrations/         # Migraciones de Alembic
static/            # Archivos estáticos
templates/         # Templates (si se usa)
```

### Nuevos Archivos

- `app/config.py` - Configuración centralizada
- `app/exceptions.py` - Excepciones custom
- `app/utils/logger.py` - Logger configurado
- `app/utils/cache.py` - Sistema de cache
- `tests/conftest.py` - Fixtures de pytest

---

## Comandos para Navegar

```bash
# Ver estructura
tree -L 2 -I 'venv|__pycache__|.git'

# Contar líneas de código
find app -name "*.py" | xargs wc -l

# Ver imports
grep -r "^import\|^from" app/*.py

# Buscar TODO
grep -r "TODO\|FIXME" app/

# Ver tamaño de archivos
du -sh app/* docs/*
```

---

## Recursos Adicionales

- **Arquitectura completa:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Setup inicial:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Uso de API:** [API_GUIDE.md](API_GUIDE.md)
- **Frontend specs:** [FRONTEND_REQUIREMENTS.md](FRONTEND_REQUIREMENTS.md)

---

**Última actualización:** 6 de diciembre de 2024
**Versión:** 0.1.0
