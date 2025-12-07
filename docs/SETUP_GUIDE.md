# Guía de Instalación y Configuración - MSPriceEngine

## Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Rutas Importantes del Proyecto](#rutas-importantes-del-proyecto)
3. [Instalación](#instalación)
4. [Configuración del Ambiente Virtual](#configuración-del-ambiente-virtual)
5. [Dependencias](#dependencias)
6. [Variables de Entorno](#variables-de-entorno)
7. [Inicialización de la Base de Datos](#inicialización-de-la-base-de-datos)
8. [Ejecutar el Servidor](#ejecutar-el-servidor)
9. [Verificar la Instalación](#verificar-la-instalación)
10. [Docker Setup](#docker-setup)
11. [Troubleshooting](#troubleshooting)

---

## Requisitos del Sistema

### Software Necesario

| Software | Versión Mínima | Recomendada | Notas |
|----------|----------------|-------------|-------|
| Python | 3.11 | 3.13 | Requerido |
| pip | 20.0 | Última | Requerido |
| Git | 2.0 | Última | Requerido |
| Docker | 20.0 | Última | Opcional |
| Docker Compose | 2.0 | Última | Opcional |

### Sistema Operativo

- Linux (Ubuntu 20.04+, Fedora 35+, etc.)
- macOS 11+
- Windows 10/11 (con WSL2 recomendado)

### Hardware Mínimo

- RAM: 2 GB
- Disco: 500 MB libres
- Procesador: Dual-core 1.5 GHz

---

## Rutas Importantes del Proyecto

### Estructura Completa

```
📁 MSPriceEngine/
├── 📂 app/                           ← Código principal de la API
│   ├── __init__.py                  ← Inicialización del paquete
│   ├── main.py                      ← Aplicación FastAPI (endpoints)
│   ├── models.py                    ← Modelos SQLAlchemy (Store, Product)
│   ├── schemas.py                   ← Esquemas Pydantic (validación)
│   ├── database.py                  ← Configuración de BD
│   ├── scheduler.py                 ← APScheduler para scraping
│   └── 📂 scrapers/                 ← Módulos de scraping
│       ├── __init__.py
│       ├── base.py                  ← Clase base para scrapers
│       ├── amazon.py                ← Scraper de Amazon MX
│       ├── walmart.py               ← Scraper de Walmart MX
│       └── liverpool.py             ← Scraper de Liverpool
│
├── 📂 data/                          ← Base de datos SQLite (creada automáticamente)
│   └── price_search.db              ← Archivo de base de datos
│
├── 📂 docs/                          ← Documentación
│   ├── ARCHITECTURE.md              ← Arquitectura técnica completa
│   ├── API_GUIDE.md                 ← Guía de uso de la API
│   ├── API_ENDPOINTS.md             ← Referencia de endpoints
│   ├── SETUP_GUIDE.md               ← Esta guía
│   └── FRONTEND_REQUIREMENTS.md     ← Especificaciones del frontend
│
├── 📂 tests/                         ← Tests automatizados
│   ├── __init__.py
│   └── test_api.py                  ← Tests de la API
│
├── 📂 venv/                          ← Ambiente virtual de Python
│   ├── bin/                         ← Ejecutables (activate, python, pip)
│   ├── lib/                         ← Librerías instaladas
│   └── ...
│
├── requirements.txt                  ← Dependencias de Python
├── .env.example                      ← Ejemplo de variables de entorno
├── .gitignore                        ← Archivos ignorados por Git
├── Dockerfile                        ← Configuración Docker
├── docker-compose.yml                ← Docker Compose setup
├── LICENSE                           ← Licencia MIT
├── README.md                         ← Documentación principal
├── test_api_manual.py                ← Script de pruebas manuales
└── RESUMEN_COMPLETO.md               ← Resumen ejecutivo del proyecto
```

### Rutas Clave para Desarrollo

| Ruta | Descripción |
|------|-------------|
| `/home/yochi/Documents/MSPriceEngine/` | Directorio raíz del proyecto |
| `/home/yochi/Documents/MSPriceEngine/venv/` | Ambiente virtual |
| `/home/yochi/Documents/MSPriceEngine/app/main.py` | Punto de entrada de la API |
| `/home/yochi/Documents/MSPriceEngine/data/` | Base de datos SQLite |
| `/home/yochi/Documents/MSPriceEngine/requirements.txt` | Dependencias |

---

## Instalación

### 1. Clonar el Repositorio

```bash
# Via SSH (recomendado si tienes SSH configurado)
git clone git@github.com:yochi2005/MSPriceEngine.git

# Via HTTPS
git clone https://github.com/yochi2005/MSPriceEngine.git

# Entrar al directorio
cd MSPriceEngine
```

### 2. Verificar Python

```bash
# Verificar versión de Python
python3 --version
# Debe mostrar: Python 3.11.x o superior

# Si no tienes Python 3.11+, instalar:
# Ubuntu/Debian
sudo apt update && sudo apt install python3.11 python3.11-venv

# Fedora
sudo dnf install python3.11

# macOS (con Homebrew)
brew install python@3.11
```

---

## Configuración del Ambiente Virtual

### ¿Qué es un Ambiente Virtual?

Un ambiente virtual (venv) es un **directorio aislado** que contiene:
- Una copia de Python
- pip (gestor de paquetes)
- Todas las dependencias del proyecto

**Ventajas:**
- No contamina el Python global del sistema
- Cada proyecto tiene sus propias dependencias
- Evita conflictos entre versiones

### Crear Ambiente Virtual

```bash
# Estar en el directorio del proyecto
cd ~/Documents/MSPriceEngine

# Crear ambiente virtual
python3 -m venv venv

# Esto crea la carpeta venv/ con:
# venv/bin/       ← Ejecutables (python, pip, activate)
# venv/lib/       ← Librerías instaladas
# venv/include/   ← Headers
```

### Activar Ambiente Virtual

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Deberías ver (venv) al inicio de tu prompt:
# (venv) user@host:~/Documents/MSPriceEngine$
```

**Importante:** Siempre activa el venv antes de trabajar con el proyecto.

### Desactivar Ambiente Virtual

```bash
deactivate
```

---

## Dependencias

### Ver Dependencias

```bash
# Ver archivo de dependencias
cat requirements.txt
```

**Contenido de `requirements.txt`:**

```
# FastAPI and web server
fastapi==0.110.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy>=2.0.36
alembic==1.13.1

# HTTP client and scraping
httpx==0.26.0
beautifulsoup4==4.12.3
html5lib==1.1

# Scheduling
apscheduler==3.10.4

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.9

# Development dependencies
pytest==8.0.0
pytest-asyncio==0.23.5
```

### Instalar Dependencias

```bash
# Asegúrate de tener el venv activado
source venv/bin/activate

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

### Actualizar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Actualizar una dependencia específica
pip install --upgrade fastapi

# Actualizar todas (cuidado, puede romper compatibilidad)
pip install --upgrade -r requirements.txt
```

### Agregar Nueva Dependencia

```bash
# Instalar nueva librería
pip install requests

# Agregar al requirements.txt
pip freeze | grep requests >> requirements.txt

# O editar requirements.txt manualmente
```

---

## Variables de Entorno

### Crear Archivo .env

```bash
# Copiar ejemplo
cp .env.example .env

# Editar con tu editor favorito
nano .env
# o
vim .env
# o
code .env  # VSCode
```

### Contenido de .env

```bash
# Base de Datos
DATABASE_URL=sqlite:///./data/price_search.db

# Para PostgreSQL (comentado por defecto):
# DATABASE_URL=postgresql://user:password@localhost:5432/priceengine

# Configuración de la Aplicación
LOG_LEVEL=INFO

# Scheduler
ENABLE_SCHEDULER=false
SCRAPING_HOUR=3
```

### Variables Disponibles

| Variable | Descripción | Valor por Defecto | Requerida |
|----------|-------------|-------------------|-----------|
| `DATABASE_URL` | URL de conexión a BD | `sqlite:///./data/price_search.db` | No |
| `LOG_LEVEL` | Nivel de logging | `INFO` | No |
| `ENABLE_SCHEDULER` | Activar scheduler automático | `false` | No |
| `SCRAPING_HOUR` | Hora del scraping diario (0-23) | `3` | No |

---

## Inicialización de la Base de Datos

### SQLite (Por Defecto)

La base de datos SQLite se crea automáticamente al iniciar la aplicación.

```bash
# Activar venv
source venv/bin/activate

# Iniciar servidor (esto crea la BD)
uvicorn app.main:app

# La BD se creará en: data/price_search.db
```

### Verificar Base de Datos

```bash
# Ver archivo de BD
ls -lh data/price_search.db

# Conectar con sqlite3 (si lo tienes instalado)
sqlite3 data/price_search.db

# Comandos SQLite:
.tables          # Ver tablas
.schema stores   # Ver estructura de tabla stores
SELECT * FROM stores;  # Ver datos
.quit            # Salir
```

### PostgreSQL (Opcional - Producción)

```bash
# 1. Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib  # Ubuntu
# o
brew install postgresql  # macOS

# 2. Crear base de datos
sudo -u postgres psql
CREATE DATABASE priceengine;
CREATE USER priceuser WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE priceengine TO priceuser;
\q

# 3. Actualizar .env
DATABASE_URL=postgresql://priceuser:password123@localhost:5432/priceengine

# 4. Instalar driver de PostgreSQL
pip install psycopg2-binary

# 5. Ejecutar migraciones (si usas Alembic)
alembic upgrade head
```

---

## Ejecutar el Servidor

### Modo Desarrollo (con auto-reload)

```bash
# Activar venv
source venv/bin/activate

# Iniciar servidor
uvicorn app.main:app --reload

# Opciones adicionales:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# El servidor estará disponible en:
# http://localhost:8000
```

**Argumentos:**
- `--reload`: Reinicia automáticamente al detectar cambios
- `--host 0.0.0.0`: Accesible desde cualquier IP (útil en red local)
- `--port 8000`: Puerto (default 8000)

### Modo Producción

```bash
# Sin reload, con workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# O con gunicorn (más robusto)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Background (Daemon)

```bash
# Con nohup
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Ver log
tail -f nohup.out

# Detener
pkill -f uvicorn
```

---

## Verificar la Instalación

### 1. Check de Salud

```bash
# Con curl
curl http://localhost:8000/health

# Debería retornar:
# {"status":"healthy"}
```

### 2. Verificar Swagger UI

Abrir navegador en: http://localhost:8000/docs

Deberías ver la documentación interactiva de la API.

### 3. Ejecutar Tests

```bash
# Activar venv
source venv/bin/activate

# Ejecutar tests automáticos
pytest

# Ejecutar test manual
python test_api_manual.py

# Deberías ver:
# ✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE
```

### 4. Test Manual con cURL

```bash
# Buscar productos (debería estar vacío inicialmente)
curl http://localhost:8000/search?q=laptop

# Ver tiendas (debería estar vacío inicialmente)
curl http://localhost:8000/stores
```

---

## Docker Setup

### Construcción de Imagen

```bash
# Build imagen
docker build -t mspriceengine .

# Verificar imagen
docker images | grep mspriceengine
```

### Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up

# Iniciar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Acceder al Contenedor

```bash
# Ejecutar bash en contenedor
docker-compose exec api bash

# Desde ahí puedes:
python -m pytest
python test_api_manual.py
```

---

## Troubleshooting

### Problema: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solución:**
```bash
# Activar venv
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: Puerto en Uso

```
ERROR: [Errno 98] Address already in use
```

**Solución:**
```bash
# Ver qué proceso usa el puerto 8000
lsof -i :8000

# Matar proceso
kill -9 <PID>

# O usar otro puerto
uvicorn app.main:app --port 8001
```

### Problema: SQLite Database is Locked

**Solución:**
```bash
# Cerrar todas las conexiones
pkill -f uvicorn
pkill -f python

# Eliminar lock
rm data/price_search.db-journal

# Reiniciar servidor
```

### Problema: Python Version Incorrecta

**Solución:**
```bash
# Verificar versión
python3 --version

# Usar versión específica
python3.11 -m venv venv
```

### Problema: Permisos Denegados

```bash
# Dar permisos de ejecución
chmod +x venv/bin/activate

# O ejecutar como superusuario (no recomendado)
sudo python3 -m venv venv
```

---

## Comandos Útiles Resumidos

```bash
# Setup inicial
git clone <repo>
cd MSPriceEngine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Desarrollo diario
source venv/bin/activate               # Activar venv
uvicorn app.main:app --reload          # Iniciar servidor
pytest                                 # Ejecutar tests
deactivate                             # Desactivar venv

# Docker
docker-compose up                      # Iniciar con Docker
docker-compose down                    # Detener

# Actualizar dependencias
pip install --upgrade <package>
pip freeze > requirements.txt

# Git
git pull                               # Actualizar código
git add .
git commit -m "mensaje"
git push
```

---

## Próximos Pasos

1. ✅ Instalación completada
2. → Leer [API_GUIDE.md](API_GUIDE.md) para aprender a usar la API
3. → Ver [API_ENDPOINTS.md](API_ENDPOINTS.md) para referencia de endpoints
4. → Leer [ARCHITECTURE.md](ARCHITECTURE.md) para entender la arquitectura
5. → Comenzar a desarrollar el frontend (ver [FRONTEND_REQUIREMENTS.md](FRONTEND_REQUIREMENTS.md))

---

**Última actualización:** 6 de diciembre de 2024
**Versión:** 0.1.0
