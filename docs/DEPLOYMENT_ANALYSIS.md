# Análisis de Deployment y Stack Tecnológico - MSPriceEngine

## Objetivo

Determinar el mejor stack tecnológico y plataformas de hosting **gratuitas** para:
1. **Backend (API)** - FastAPI ya desarrollado
2. **Frontend (Web App)** - Por desarrollar
3. **Base de Datos** - PostgreSQL/SQLite

---

## Opciones de Hosting Gratuito

### Para Frontend (Static Sites)

#### 1. Cloudflare Pages ⭐ RECOMENDADO

**Ventajas:**
- ✅ **Completamente GRATIS** sin límites ridículos
- ✅ **CDN global** automático (ultra rápido en todo el mundo)
- ✅ **Build automático** desde GitHub
- ✅ **HTTPS** gratis
- ✅ **Ilimitadas** requests/builds
- ✅ **Dominio custom** gratis (tudominio.com)
- ✅ **Deployments instantáneos** (< 1 minuto)
- ✅ **Preview deployments** por cada PR
- ✅ Soporta **React, Vue, Next.js, Vite**

**Límites:**
- 500 builds/mes (más que suficiente)
- 20,000 archivos por deploy

**Precio:** $0 USD/mes

**Setup:**
```bash
# 1. Crear cuenta en cloudflare.com
# 2. Conectar repo de GitHub
# 3. Configurar build:
#    Build command: npm run build
#    Output directory: dist
# 4. Deploy automático en cada push
```

**URL final:** `mspriceengine.pages.dev` o `tudominio.com`

---

#### 2. Vercel

**Ventajas:**
- ✅ GRATIS para proyectos personales
- ✅ Deploy automático desde GitHub
- ✅ HTTPS automático
- ✅ Optimizado para Next.js/React
- ✅ Preview deployments

**Límites:**
- 100 GB bandwidth/mes
- Puede ser lento fuera de US

**Precio:** $0 USD/mes

---

#### 3. Netlify

**Ventajas:**
- ✅ GRATIS con buen tier
- ✅ Deploy desde Git
- ✅ Formularios gratis
- ✅ HTTPS automático

**Límites:**
- 100 GB bandwidth/mes
- 300 build minutes/mes

**Precio:** $0 USD/mes

---

### Para Backend (API FastAPI)

#### 1. Railway ⭐ RECOMENDADO

**Ventajas:**
- ✅ **$5 USD gratis/mes** de crédito (suficiente para desarrollo)
- ✅ Deploy desde **GitHub** automático
- ✅ Soporta **Python + PostgreSQL**
- ✅ Variables de entorno fáciles
- ✅ **Base de datos PostgreSQL incluida**
- ✅ Logs en tiempo real
- ✅ HTTPS automático
- ✅ Muy fácil de usar

**Límites:**
- $5/mes gratis = ~500 horas de ejecución
- Si se acaba el crédito, se pausa (no cobra)

**Precio:** $0-5 USD/mes (gratis con crédito)

**Setup:**
```bash
# 1. railway.app → Sign up
# 2. New Project → Deploy from GitHub
# 3. Agregar PostgreSQL (1 click)
# 4. Variables de entorno automáticas
# 5. Deploy
```

---

#### 2. Render

**Ventajas:**
- ✅ **Tier gratis** disponible
- ✅ PostgreSQL gratis (con límites)
- ✅ Deploy desde GitHub
- ✅ HTTPS automático

**Desventajas:**
- ⚠️ **Se duerme después de 15 min sin uso** (tarda 30-60s en despertar)
- ⚠️ PostgreSQL gratis expira después de 90 días

**Precio:** $0 USD/mes (con limitaciones)

---

#### 3. Fly.io

**Ventajas:**
- ✅ Tier gratis disponible
- ✅ 3 VMs pequeñas gratis
- ✅ PostgreSQL pequeña gratis
- ✅ Deploy con Docker

**Desventajas:**
- ⚠️ Requiere tarjeta de crédito (no cobra si no pasas límites)
- Más complejo de configurar

**Precio:** $0 USD/mes (con límites)

---

#### 4. PythonAnywhere (Alternativa Simple)

**Ventajas:**
- ✅ Tier gratis específico para Python
- ✅ No requiere tarjeta
- ✅ MySQL gratis incluida

**Desventajas:**
- ⚠️ Límites muy estrictos (CPU, requests)
- ⚠️ No soporta PostgreSQL en tier gratis
- ⚠️ No deploy automático

**Precio:** $0 USD/mes

---

### Para Base de Datos

#### 1. Railway PostgreSQL (con Backend)

**Incluido con Railway** - Opción más simple.

---

#### 2. Supabase ⭐ ALTERNATIVA

**Ventajas:**
- ✅ **PostgreSQL gratis** para siempre
- ✅ 500 MB almacenamiento
- ✅ API automática (REST + GraphQL)
- ✅ Authentication incluida
- ✅ No se duerme

**Límites:**
- 500 MB de datos
- 2 GB de bandwidth/mes

**Precio:** $0 USD/mes

---

#### 3. Neon

**Ventajas:**
- ✅ PostgreSQL serverless
- ✅ 0.5 GB gratis
- ✅ Escala a 0 (no consume cuando no se usa)

**Precio:** $0 USD/mes

---

## Stack Tecnológico Recomendado

### Opción 1: Todo Gratis (RECOMENDADA)

```
Frontend:
├─ Framework: React 18 + Vite
├─ Styling: TailwindCSS
├─ Hosting: Cloudflare Pages (GRATIS ∞)
└─ URL: mspriceengine.pages.dev

Backend:
├─ Framework: FastAPI (ya tenemos)
├─ Hosting: Railway ($5/mes crédito gratis)
└─ URL: mspriceengine.up.railway.app

Base de Datos:
├─ PostgreSQL en Railway (incluido)
└─ Backup: Exportar a GitHub semanalmente

Costo Total: $0/mes
```

**Ventajas:**
- Sin costo
- Railway $5/mes alcanza para ~500 horas = 24/7 con margen
- Cloudflare Pages es ilimitado
- Todo deploy automático desde GitHub

**Desventajas:**
- Si Railway se acaba el crédito ($5), la API se pausa
- Solución: Monitorear uso, optimizar, o pagar $5/mes

---

### Opción 2: Máxima Simplicidad

```
Frontend:
├─ Vite + React + TailwindCSS
├─ Hosting: Vercel (GRATIS)
└─ URL: mspriceengine.vercel.app

Backend:
├─ FastAPI
├─ Hosting: Render (GRATIS)
└─ URL: mspriceengine.onrender.com

Base de Datos:
├─ Render PostgreSQL (GRATIS 90 días)
└─ Alternativa: Supabase PostgreSQL (GRATIS ∞)

Costo Total: $0/mes
```

**Ventajas:**
- Completamente gratis
- Muy fácil de configurar

**Desventajas:**
- Render se duerme (15 min inactividad)
- Primera request tarda 30-60 segundos
- PostgreSQL de Render expira en 90 días

---

### Opción 3: Híbrida (MEJOR PERFORMANCE)

```
Frontend:
├─ Cloudflare Pages (GRATIS, ultra rápido)

Backend:
├─ Railway ($5/mes gratis, siempre activo)

Base de Datos:
├─ Supabase PostgreSQL (GRATIS ∞)

Costo Total: $0/mes
```

**Ventajas:**
- Frontend ultra rápido (CDN global de Cloudflare)
- Backend siempre despierto (Railway)
- BD gratis para siempre (Supabase)
- Sin límite de tiempo

---

## Comparación Detallada

### Frontend Hosting

| Plataforma | Gratis | Bandwidth | Builds/mes | CDN Global | Custom Domain | Recomendación |
|------------|--------|-----------|------------|------------|---------------|---------------|
| **Cloudflare Pages** | ✅ Sí | Ilimitado | 500 | ✅ Sí | ✅ Sí | ⭐⭐⭐⭐⭐ |
| Vercel | ✅ Sí | 100 GB | Ilimitado | ✅ Sí | ✅ Sí | ⭐⭐⭐⭐ |
| Netlify | ✅ Sí | 100 GB | 300 min | ✅ Sí | ✅ Sí | ⭐⭐⭐⭐ |
| GitHub Pages | ✅ Sí | 100 GB | Ilimitado | ❌ No | ✅ Sí | ⭐⭐⭐ |

**Ganador:** Cloudflare Pages

---

### Backend Hosting

| Plataforma | Gratis | Siempre Activo | PostgreSQL | Auto Deploy | Fácil Setup | Recomendación |
|------------|--------|----------------|------------|-------------|-------------|---------------|
| **Railway** | $5/mes crédito | ✅ Sí | ✅ Incluido | ✅ Sí | ✅ Muy fácil | ⭐⭐⭐⭐⭐ |
| Render | ✅ Sí | ❌ Se duerme | ✅ 90 días | ✅ Sí | ✅ Fácil | ⭐⭐⭐ |
| Fly.io | ✅ Sí | ✅ Sí | ✅ Pequeña | ✅ Sí | ⚠️ Medio | ⭐⭐⭐⭐ |
| PythonAnywhere | ✅ Sí | ✅ Sí | ❌ No | ❌ No | ⚠️ Difícil | ⭐⭐ |
| Heroku | ❌ $7/mes | - | ❌ Pago | - | - | ❌ |

**Ganador:** Railway (mejor balance costo/beneficio)

---

### Base de Datos

| Plataforma | Gratis | Tamaño | Expira | Backups | Conexiones | Recomendación |
|------------|--------|--------|--------|---------|------------|---------------|
| Railway PostgreSQL | Con Backend | 1 GB | ❌ No | ✅ Sí | Ilimitadas | ⭐⭐⭐⭐⭐ |
| **Supabase** | ✅ Sí | 500 MB | ❌ No | ✅ Sí | Ilimitadas | ⭐⭐⭐⭐⭐ |
| Render PostgreSQL | ✅ Sí | 1 GB | ✅ 90 días | ✅ Sí | 100 | ⭐⭐⭐ |
| Neon | ✅ Sí | 0.5 GB | ❌ No | ✅ Sí | Ilimitadas | ⭐⭐⭐⭐ |

**Ganador:** Railway (si usas Railway para backend) o Supabase (standalone)

---

## Recomendación Final

### Stack Recomendado (Opción Óptima)

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIOS                             │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           FRONTEND (Cloudflare Pages)                    │
│           - React + Vite + TailwindCSS                   │
│           - URL: mspriceengine.pages.dev                 │
│           - GRATIS, CDN Global, Ilimitado                │
└────────────────────┬───────────────────────────────────┘
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────┐
│           BACKEND API (Railway)                          │
│           - FastAPI + Python 3.13                        │
│           - URL: mspriceengine.up.railway.app            │
│           - $5/mes gratis, siempre activo                │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           BASE DE DATOS (Railway PostgreSQL)             │
│           - PostgreSQL 15                                │
│           - 1 GB almacenamiento                          │
│           - Incluido con Railway                         │
└─────────────────────────────────────────────────────────┘
```

**Costo Mensual:** $0 USD (usando crédito de Railway)

**Capacidad:**
- Frontend: Ilimitado
- Backend: ~500 horas/mes = 24/7 con margen
- Base de Datos: 1 GB (suficiente para ~100k productos)

---

## Plan de Deployment

### Fase 1: Frontend

```bash
# 1. Crear proyecto React
npm create vite@latest price-search-frontend -- --template react
cd price-search-frontend

# 2. Desarrollar frontend localmente

# 3. Push a GitHub
git push origin main

# 4. Conectar a Cloudflare Pages
# - Ir a dash.cloudflare.com
# - Pages → Create project
# - Connect GitHub repo
# - Build command: npm run build
# - Output: dist
# - Deploy

# URL: mspriceengine.pages.dev
```

### Fase 2: Backend

```bash
# 1. Preparar backend para producción
# - Agregar requirements.txt con psycopg2-binary
# - Configurar variables de entorno

# 2. Push a GitHub (ya lo tenemos)

# 3. Deploy en Railway
# - railway.app → New Project
# - Deploy from GitHub
# - Select MSPriceEngine repo
# - Add PostgreSQL service
# - Deploy

# URL: mspriceengine.up.railway.app
```

### Fase 3: Conectar Frontend con Backend

```javascript
// En frontend: src/services/api.js
const API_URL = import.meta.env.VITE_API_URL ||
                'https://mspriceengine.up.railway.app';
```

---

## Variables de Entorno

### Backend (Railway)

```bash
DATABASE_URL=postgresql://...  # Auto-generada por Railway
ENABLE_SCHEDULER=true
SCRAPING_HOUR=3
LOG_LEVEL=INFO
CORS_ORIGINS=https://mspriceengine.pages.dev
```

### Frontend (Cloudflare Pages)

```bash
VITE_API_URL=https://mspriceengine.up.railway.app
```

---

## Costos Proyectados

### Año 1 (Desarrollo)

| Servicio | Costo/mes | Costo/año |
|----------|-----------|-----------|
| Cloudflare Pages | $0 | $0 |
| Railway (con crédito) | $0 | $0 |
| **Total** | **$0** | **$0** |

### Año 1 (Si crece y necesitas más)

| Servicio | Costo/mes | Costo/año |
|----------|-----------|-----------|
| Cloudflare Pages | $0 | $0 |
| Railway (si se acaba crédito) | $5 | $60 |
| Dominio .com (opcional) | $1 | $12 |
| **Total** | **$6** | **$72** |

---

## Alternativas si Railway se Queda Sin Crédito

1. **Optimizar uso:**
   - Reducir workers de Uvicorn
   - Usar cache (Redis de Railway, $1/mes)
   - Limitar scraping a 1x/día

2. **Migrar a Render (gratis pero se duerme):**
   - Gratis para siempre
   - Se duerme después de 15 min
   - OK para proyectos en desarrollo

3. **Pagar Railway $5/mes:**
   - Vale la pena si el proyecto crece
   - Siempre activo, rápido, confiable

---

## Dominios

### Gratis
- `mspriceengine.pages.dev` (Cloudflare)
- `mspriceengine.up.railway.app` (Railway)

### Pagado (Opcional)
- `mspriceengine.com` - $12/año en Cloudflare
- `preciosmx.com` - $12/año
- `comparaprecios.mx` - $15/año

---

## Resumen de Recomendaciones

### ✅ Stack Final Recomendado

**Frontend:**
- Framework: **React 18 + Vite**
- Styling: **TailwindCSS**
- Hosting: **Cloudflare Pages**
- Costo: **$0/mes**

**Backend:**
- Framework: **FastAPI** (ya lo tenemos)
- Hosting: **Railway**
- Costo: **$0-5/mes** (con crédito gratis)

**Base de Datos:**
- Engine: **PostgreSQL**
- Hosting: **Railway** (incluido con backend)
- Costo: **$0/mes** (incluido)

**Costo Total:** **$0/mes** usando créditos gratuitos

---

## Próximo Paso

¿Procedemos con esta configuración?

1. ✅ Crear frontend con React + Vite
2. ✅ Deploy en Cloudflare Pages
3. ✅ Deploy backend en Railway
4. ✅ Conectar todo

---

**Fecha:** 6 de diciembre de 2024
**Versión:** 1.0
