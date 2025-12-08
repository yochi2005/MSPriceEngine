# Plan de Deployment - MSPriceEngine

## Objetivo

Desplegar MSPriceEngine (Backend + Frontend) a producción usando servicios gratuitos sin costo mensual.

---

## Stack de Deployment Elegido

### Backend API
- **Plataforma:** Railway
- **Costo:** $0/mes (usando $5 crédito mensual gratis)
- **Base de datos:** PostgreSQL incluida en Railway
- **URL final:** `mspriceengine.up.railway.app`

### Frontend
- **Plataforma:** Cloudflare Pages
- **Costo:** $0/mes (tier gratuito ilimitado)
- **URL final:** `mspriceengine-frontend.pages.dev`

### Dominio (Opcional - Futuro)
- **Registrar:** `mspriceengine.com` o `preciosmx.com`
- **Costo:** ~$12/año en Cloudflare
- **DNS:** Cloudflare (gratis)

---

## Fase 1: Preparación del Backend

### 1.1 Mergear Branch Feature a Main

```bash
cd ~/Documents/MSPriceEngine

# Cambiar a main
git checkout main

# Mergear feature branch
git merge feature/add-cors-and-docs

# Push a main
git push origin main
```

### 1.2 Verificar Archivos para Producción

**Archivos necesarios:**
- ✅ `requirements.txt` - Ya existe
- ✅ `Dockerfile` - Ya existe (opcional para Railway)
- ✅ `.gitignore` - Ya existe
- ⚠️ Necesita: `railway.json` o `Procfile`

### 1.3 Crear Procfile para Railway

```bash
# Crear Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

### 1.4 Actualizar CORS para Producción

Editar `app/main.py`:

```python
# Agregar URL de producción a CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://mspriceengine-frontend.pages.dev",  # URL de producción
        "https://mspriceengine.com",  # Dominio custom (futuro)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 1.5 Actualizar requirements.txt para PostgreSQL

Verificar que incluya:
```
psycopg2-binary>=2.9.9  # Para PostgreSQL en producción
```

---

## Fase 2: Deploy Backend en Railway

### 2.1 Crear Cuenta en Railway

1. Ir a https://railway.app
2. Sign up con GitHub
3. Autorizar acceso a repositorios

### 2.2 Crear Nuevo Proyecto

1. Click en "New Project"
2. Seleccionar "Deploy from GitHub repo"
3. Elegir repositorio: `yochi2005/MSPriceEngine`
4. Branch: `main`

### 2.3 Agregar PostgreSQL

1. En el proyecto, click "New"
2. Seleccionar "Database" → "PostgreSQL"
3. Railway automáticamente:
   - Crea la base de datos
   - Genera variable `DATABASE_URL`
   - La conecta al servicio

### 2.4 Configurar Variables de Entorno

En Railway → Settings → Variables:

```bash
# Automática (Railway la genera)
DATABASE_URL=postgresql://...

# Configurar manualmente
ENABLE_SCHEDULER=true
SCRAPING_HOUR=3
LOG_LEVEL=INFO
CORS_ORIGINS=https://mspriceengine-frontend.pages.dev
```

### 2.5 Configurar Build

Railway detecta automáticamente:
- `requirements.txt` → Instala Python dependencies
- `Procfile` → Ejecuta el comando especificado
- Puerto → Usa variable `$PORT`

**Build Command (automático):**
```bash
pip install -r requirements.txt
```

**Start Command (desde Procfile):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2.6 Deploy

1. Railway hace deploy automático
2. Esperar 2-3 minutos
3. Ver logs en tiempo real
4. Verificar que inicie sin errores

### 2.7 Obtener URL Pública

1. En Railway → Settings → Domains
2. Click "Generate Domain"
3. Railway genera: `mspriceengine.up.railway.app`
4. O configurar dominio custom

### 2.8 Verificar Deployment

```bash
# Health check
curl https://mspriceengine.up.railway.app/health

# Verificar docs
# Abrir: https://mspriceengine.up.railway.app/docs

# Test search (estará vacío inicialmente)
curl "https://mspriceengine.up.railway.app/search?q=laptop"
```

---

## Fase 3: Preparación del Frontend

### 3.1 Actualizar Variables de Entorno

Editar `.env` local para testing:
```bash
VITE_API_URL=https://mspriceengine.up.railway.app
```

### 3.2 Probar Conexión Local con Backend de Producción

```bash
cd ~/Documents/mspriceengine-frontend

# Actualizar .env
echo "VITE_API_URL=https://mspriceengine.up.railway.app" > .env

# Ejecutar
npm run dev

# Probar en http://localhost:5174
# Debería conectarse al backend en Railway
```

### 3.3 Hacer Build de Producción Local (Test)

```bash
npm run build

# Verificar que no haya errores
# Output en: dist/
```

### 3.4 Commit de Cambios (si hay)

```bash
git add .
git commit -m "Update API URL for production deployment"
git push origin main
```

---

## Fase 4: Deploy Frontend en Cloudflare Pages

### 4.1 Crear Cuenta en Cloudflare

1. Ir a https://dash.cloudflare.com
2. Sign up / Login
3. Ir a "Pages" en el menú lateral

### 4.2 Crear Nuevo Proyecto

1. Click "Create a project"
2. Click "Connect to Git"
3. Autorizar GitHub
4. Seleccionar repositorio: `yochi2005/MSPriceEngineFrontend`

### 4.3 Configurar Build Settings

**Framework preset:** Vite

**Build command:**
```bash
npm run build
```

**Build output directory:**
```
dist
```

**Root directory:**
```
/
```

**Install command (opcional, auto-detectado):**
```bash
npm install
```

### 4.4 Configurar Variables de Entorno

En Cloudflare Pages → Settings → Environment variables:

**Production:**
```bash
VITE_API_URL=https://mspriceengine.up.railway.app
```

**Preview (opcional, para PRs):**
```bash
VITE_API_URL=https://mspriceengine.up.railway.app
```

### 4.5 Deploy

1. Click "Save and Deploy"
2. Cloudflare construye el proyecto
3. Esperar 1-2 minutos
4. Ver logs de build

### 4.6 Obtener URL

Cloudflare genera:
- **Production:** `https://mspriceengine-frontend.pages.dev`
- **Preview (por PR):** `https://[commit-hash].mspriceengine-frontend.pages.dev`

### 4.7 Configurar Dominio Custom (Opcional - Futuro)

1. En Cloudflare Pages → Custom domains
2. Click "Set up a custom domain"
3. Ingresar: `mspriceengine.com`
4. Cloudflare configura DNS automáticamente

---

## Fase 5: Verificación Post-Deployment

### 5.1 Verificar Backend

```bash
# Health check
curl https://mspriceengine.up.railway.app/health
# Esperado: {"status":"healthy"}

# API docs
# Abrir: https://mspriceengine.up.railway.app/docs

# Stores endpoint
curl https://mspriceengine.up.railway.app/stores
# Esperado: [] o lista de tiendas

# Search endpoint
curl "https://mspriceengine.up.railway.app/search?q=laptop"
# Esperado: {"total":0,"products":[]} (vacío al inicio)
```

### 5.2 Verificar Frontend

1. Abrir: `https://mspriceengine-frontend.pages.dev`
2. Verificar que cargue el hero section
3. Intentar buscar "laptop"
4. Debería mostrar "No hay resultados" (base de datos vacía)
5. Verificar responsive (mobile, tablet, desktop)

### 5.3 Verificar Integración Frontend-Backend

**Abrir DevTools (F12) en el frontend:**

1. Ir a Network tab
2. Buscar "laptop"
3. Verificar request a: `https://mspriceengine.up.railway.app/search?q=laptop`
4. Verificar status: `200 OK`
5. Verificar response: `{"total":0,"products":[]}`
6. **NO debe haber errores CORS**

### 5.4 Poblar Base de Datos en Producción

**Opción A: Ejecutar scraper manualmente (Railway CLI)**

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link al proyecto
railway link

# Ejecutar comando en producción
railway run python -c "from app.scheduler import scheduler; scheduler.run_now()"
```

**Opción B: Activar scheduler automático**

Ya está configurado con `ENABLE_SCHEDULER=true`, correrá a las 3:00 AM diariamente.

**Opción C: Agregar productos de prueba mediante API**

Crear un script para poblar vía API (futuro endpoint POST).

---

## Fase 6: Configuración de Auto-Deploy

### 6.1 Backend (Railway)

**Ya configurado automáticamente:**
- Cada push a `main` → Deploy automático
- Railway detecta cambios en GitHub
- Build y deploy en ~2-3 minutos

**Verificar:**
1. Railway → Settings → GitHub
2. Debe estar conectado a `yochi2005/MSPriceEngine`
3. Branch: `main`
4. Auto-deploy: Enabled

### 6.2 Frontend (Cloudflare Pages)

**Ya configurado automáticamente:**
- Cada push a `main` → Deploy automático
- Cloudflare detecta cambios en GitHub
- Build y deploy en ~1-2 minutos

**Configuración de Preview Deployments:**
- Cada Pull Request → Preview URL automático
- Útil para testing antes de mergear

**Verificar:**
1. Cloudflare Pages → Settings → Builds & deployments
2. Debe estar conectado a `yochi2005/MSPriceEngineFrontend`
3. Production branch: `main`
4. Auto-deploy: Enabled

---

## Fase 7: Monitoreo y Mantenimiento

### 7.1 Monitoreo de Railway

**Logs:**
1. Railway → Deployments → View logs
2. Ver logs en tiempo real
3. Buscar errores

**Métricas:**
1. Railway → Metrics
2. CPU usage
3. Memory usage
4. Network usage

**Límites:**
```
CPU: Compartido
RAM: 512MB - 1GB
Disco: 1GB (PostgreSQL)
Ancho de banda: Ilimitado
Horas de ejecución: ~500h/mes con $5 crédito
```

### 7.2 Monitoreo de Cloudflare Pages

**Analytics:**
1. Cloudflare Pages → Analytics
2. Page views
3. Requests
4. Bandwidth usage

**Build History:**
1. Ver todos los deploys
2. Rollback a versión anterior si necesario

### 7.3 Monitoreo de Base de Datos

**Railway PostgreSQL:**
1. Railway → PostgreSQL service → Metrics
2. Disk usage
3. Conexiones activas
4. Query performance (futuro)

**Backups:**
- Railway hace backups automáticos
- Retención: 7 días (tier gratis)

### 7.4 Alertas (Opcional)

**Railway:**
- Configurable vía email o Slack
- Alertas de crash, deploy fallido, uso de recursos

**Cloudflare:**
- Alertas de deploy fallido
- Alertas de uso excesivo

---

## Fase 8: Troubleshooting

### 8.1 Backend no Inicia

**Error:** Application failed to start

**Solución:**
```bash
# Ver logs en Railway
# Verificar:
1. requirements.txt tiene todas las dependencias
2. Procfile tiene comando correcto
3. PORT variable está siendo usada
4. DATABASE_URL está configurada
```

**Comando correcto en Procfile:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 8.2 Error de CORS

**Error:** "blocked by CORS policy"

**Solución:**
```python
# En app/main.py, agregar URL de Cloudflare
allow_origins=[
    "https://mspriceengine-frontend.pages.dev",
    "http://localhost:5174",
]
```

### 8.3 Base de Datos Vacía

**Problema:** No hay productos en búsquedas

**Solución:**
```bash
# Opción 1: Ejecutar scraper manualmente
railway run python -c "from app.scheduler import scheduler; scheduler.run_now()"

# Opción 2: Esperar a las 3:00 AM (scheduler automático)

# Opción 3: Verificar que ENABLE_SCHEDULER=true
```

### 8.4 Build Falla en Cloudflare

**Error:** Build command failed

**Solución:**
```bash
# Verificar:
1. package.json tiene "build": "vite build"
2. Todas las dependencias están en package.json
3. No hay errores de sintaxis en código
4. Variables de entorno están configuradas
```

### 8.5 Frontend no Conecta con Backend

**Error:** Network error, failed to fetch

**Solución:**
```bash
# 1. Verificar variable de entorno en Cloudflare
VITE_API_URL=https://mspriceengine.up.railway.app

# 2. Rebuild el frontend después de cambiar variables
# Cloudflare Pages → Deployments → Retry deployment

# 3. Verificar CORS en backend
```

---

## Fase 9: Optimizaciones Post-Deploy

### 9.1 Backend

**Cache de Búsquedas (Futuro):**
```python
# Usar Redis de Railway ($1/mes adicional)
# O cache in-memory simple
from functools import lru_cache

@lru_cache(maxsize=1000)
def search_products_cached(query: str):
    # Cachea resultados por 5 minutos
    pass
```

**Optimizar Queries:**
```python
# Agregar índices en base de datos
# models.py
class Product(Base):
    name = Column(String, index=True)  # Ya existe
    price = Column(Float, index=True)  # Agregar
```

**Rate Limiting:**
```python
# Proteger contra abuso
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/search")
@limiter.limit("100/minute")
def search_products(...):
    pass
```

### 9.2 Frontend

**Code Splitting:**
```javascript
// React.lazy para componentes grandes
const ProductGrid = lazy(() => import('./components/ProductGrid'));
```

**Image Optimization:**
```javascript
// Usar WebP, lazy loading
<img loading="lazy" />
```

**Service Worker (PWA):**
```javascript
// Vite PWA plugin para offline support
npm install vite-plugin-pwa
```

### 9.3 Base de Datos

**Limpiar Productos Viejos:**
```sql
-- Borrar productos de más de 30 días
DELETE FROM products
WHERE last_updated < NOW() - INTERVAL '30 days';
```

**Vacuum PostgreSQL:**
```sql
-- Optimizar espacio
VACUUM ANALYZE;
```

---

## Fase 10: Costos Proyectados

### Año 1 (Gratis)

| Servicio | Costo/mes | Límites |
|----------|-----------|---------|
| Railway (Backend + DB) | $0 | $5 crédito/mes ≈ 500h |
| Cloudflare Pages | $0 | Ilimitado |
| **Total** | **$0** | - |

### Año 1 (Si Crece)

| Servicio | Costo/mes | Beneficio |
|----------|-----------|-----------|
| Railway | $5 | Sin límite de horas |
| Cloudflare Pages | $0 | Ilimitado |
| Dominio .com | $1 | Profesional |
| **Total** | **$6** | - |

### Escalabilidad (Futuro)

| Servicio | Costo/mes | Capacidad |
|----------|-----------|-----------|
| Railway Pro | $20 | 8GB RAM, más CPU |
| Redis (Railway) | $1 | Cache rápido |
| Cloudflare Pro | $20 | Analytics avanzados |
| **Total escalado** | **$41** | ~100k usuarios/mes |

---

## Checklist de Deployment

### Pre-Deploy

- [ ] Backend mergeado a main
- [ ] Frontend en repositorio separado
- [ ] `Procfile` creado
- [ ] CORS actualizado con URLs de producción
- [ ] Variables de entorno documentadas
- [ ] `.env.example` actualizado
- [ ] `requirements.txt` incluye `psycopg2-binary`

### Deploy Backend

- [ ] Cuenta Railway creada
- [ ] Proyecto creado desde GitHub
- [ ] PostgreSQL agregada
- [ ] Variables de entorno configuradas
- [ ] Deploy exitoso
- [ ] URL pública generada
- [ ] Health check funciona
- [ ] API docs accesibles

### Deploy Frontend

- [ ] Cuenta Cloudflare creada
- [ ] Proyecto creado desde GitHub
- [ ] Build settings configurados
- [ ] Variable `VITE_API_URL` configurada
- [ ] Deploy exitoso
- [ ] URL pública generada
- [ ] Frontend carga correctamente

### Post-Deploy

- [ ] Frontend conecta con backend (sin CORS errors)
- [ ] Búsquedas funcionan
- [ ] Responsive funciona (mobile, tablet, desktop)
- [ ] Auto-deploy configurado en ambos servicios
- [ ] Logs monitoreados
- [ ] Scheduler activado (o productos agregados manualmente)

### Opcional

- [ ] Dominio custom configurado
- [ ] SSL/HTTPS funcionando (automático en ambos)
- [ ] Analytics configurado
- [ ] Alertas de monitoring configuradas
- [ ] Backups verificados

---

## URLs Finales

### Desarrollo
```
Backend:  http://localhost:8000
Frontend: http://localhost:5174
API Docs: http://localhost:8000/docs
```

### Producción
```
Backend:  https://mspriceengine.up.railway.app
Frontend: https://mspriceengine-frontend.pages.dev
API Docs: https://mspriceengine.up.railway.app/docs
```

### Futuro (con dominio custom)
```
Frontend: https://mspriceengine.com
Backend:  https://api.mspriceengine.com
```

---

## Soporte y Recursos

### Railway
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://status.railway.app

### Cloudflare Pages
- Docs: https://developers.cloudflare.com/pages
- Community: https://community.cloudflare.com
- Status: https://www.cloudflarestatus.com

### PostgreSQL
- Railway Postgres: https://docs.railway.app/databases/postgresql
- Connection string: Auto-generado por Railway

---

## Próximos Pasos Después del Deploy

1. **Poblar base de datos**
   - Ejecutar scraper inicial
   - Agregar productos de prueba

2. **Monitorear primeras 24 horas**
   - Ver logs de errores
   - Verificar uso de recursos
   - Confirmar scheduler funciona

3. **Optimizar según uso**
   - Agregar índices si queries son lentas
   - Activar cache si hay muchas búsquedas repetidas

4. **Completar scrapers**
   - Walmart MX (requiere JavaScript rendering)
   - Liverpool
   - Más tiendas

5. **Features adicionales**
   - Historial de precios
   - Alertas de precio
   - Comparación lado a lado
   - Filtros avanzados

---

**Fecha de Creación:** 7 de diciembre de 2024
**Versión:** 1.0
**Autor:** MSPriceEngine Team
**Estado:** Listo para ejecutar
