# Guía de Credenciales de API

Este documento explica cómo obtener y configurar credenciales para cada tienda.

---

## 🛒 Mercado Libre

**Estado:** ✅ Funcional (API pública sin autenticación)

### Configuración:
```python
from app.integrations.stores.mercadolibre import MercadoLibreIntegration

ml = MercadoLibreIntegration()
products = await ml.fetch_products(query="laptop")
```

**No requiere credenciales** - La API de búsqueda es pública.

---

## 📦 Amazon Mexico

**Estado:** ⚠️ Requiere registro

### Paso 1: Registrarse en Amazon Associates
1. Ir a https://affiliate-program.amazon.com.mx/
2. Crear cuenta de Amazon Associates
3. Obtener **Partner Tag** (Associate ID)

### Paso 2: Registrarse en Product Advertising API
1. Ir a https://webservices.amazon.com/paapi5/documentation/
2. Registrarse para PA-API 5.0
3. Obtener:
   - **Access Key**
   - **Secret Key**

### Paso 3: Configuración
```python
from app.integrations.stores.amazon import AmazonMXIntegration

config = {
    'access_key': 'TU_AWS_ACCESS_KEY',
    'secret_key': 'TU_AWS_SECRET_KEY',
    'partner_tag': 'TU_ASSOCIATE_ID'
}

amazon = AmazonMXIntegration(config=config)
products = await amazon.fetch_products(query="laptop")
```

### Variables de Entorno (Recomendado):
```bash
# .env
AMAZON_ACCESS_KEY=tu_access_key_aqui
AMAZON_SECRET_KEY=tu_secret_key_aqui
AMAZON_PARTNER_TAG=tu_partner_tag_aqui
```

**Límites de API:**
- 1 request por segundo
- 8640 requests por día (gratis)
- Requiere 3 ventas calificadas en 180 días

**Documentación:**
- https://webservices.amazon.com/paapi5/documentation/

---

## 🏪 Walmart Mexico

**Estado:** ⚠️ No tiene API pública oficial

### Opciones:

#### Opción 1: Contactar a Walmart para Feed
Si eres partner de Walmart, podrían proporcionar:
- Feed CSV
- Feed XML
- API privada

**Contacto:** https://www.walmartmexico.com/contacto

#### Opción 2: API Interna (No recomendado)
Walmart usa GraphQL internamente, pero no es una API oficial y puede cambiar.

**No implementado por defecto** - Requiere investigación adicional y cumplir términos de servicio.

### Configuración (cuando esté disponible):
```python
from app.integrations.stores.walmart import WalmartCSVIntegration

config = {
    'feed_url': 'https://walmart.com.mx/feeds/products.csv'
}

walmart = WalmartCSVIntegration(config=config)
```

---

## 🎯 Liverpool

**Estado:** ⚠️ No tiene API pública oficial

### Opciones:

#### Opción 1: Feed para Partners
Liverpool podría proporcionar feeds para partners comerciales.

**Contacto:** https://www.liverpool.com.mx/

#### Opción 2: Solicitar API
Contactar directamente a Liverpool para solicitar acceso a API.

### Configuración (cuando esté disponible):
```python
from app.integrations.stores.liverpool import LiverpoolIntegration

config = {
    'feed_url': 'https://liverpool.com.mx/api/products.json',
    'api_key': 'tu_api_key_aqui'  # Si se requiere
}

liverpool = LiverpoolIntegration(config=config)
products = await liverpool.fetch_products(query="laptop")
```

---

## 🏬 Coppel

**Estado:** ⚠️ Requiere feed URL

### Paso 1: Obtener Feed
Contactar a Coppel para solicitar:
- Feed JSON de productos
- Feed XML de productos

### Paso 2: Configuración
```python
from app.integrations.stores.coppel import CoppelIntegration

config = {
    'feed_url': 'https://coppel.com/api/products.json',
    'product_path': 'data.items'  # Ruta a productos en JSON
}

coppel = CoppelIntegration(config=config)
products = await coppel.fetch_products()
```

---

## 🔧 Sears Mexico

**Estado:** ⚠️ Requiere feed URL

### Paso 1: Obtener Feed XML
Sears podría proporcionar feed Google Merchant Center:
- Feed XML (Google Shopping)
- Feed personalizado

### Paso 2: Configuración
```python
from app.integrations.stores.sears import SearsIntegration

config = {
    'feed_url': 'https://sears.com.mx/feed/products.xml'
}

sears = SearsIntegration(config=config)
products = await sears.fetch_products(query="laptop")
```

---

## ⚙️ Configuración Global

### Usando Variables de Entorno:

```bash
# .env
# Mercado Libre (no requiere credenciales)

# Amazon
AMAZON_ACCESS_KEY=your_key
AMAZON_SECRET_KEY=your_secret
AMAZON_PARTNER_TAG=your_tag

# Coppel
COPPEL_FEED_URL=https://...

# Sears
SEARS_FEED_URL=https://...

# Liverpool
LIVERPOOL_FEED_URL=https://...
LIVERPOOL_API_KEY=optional_key

# Walmart
WALMART_FEED_URL=https://...
```

### Cargar Configuración:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Amazon
amazon_config = {
    'access_key': os.getenv('AMAZON_ACCESS_KEY'),
    'secret_key': os.getenv('AMAZON_SECRET_KEY'),
    'partner_tag': os.getenv('AMAZON_PARTNER_TAG')
}

# Coppel
coppel_config = {
    'feed_url': os.getenv('COPPEL_FEED_URL')
}

# Sears
sears_config = {
    'feed_url': os.getenv('SEARS_FEED_URL')
}

# Liverpool
liverpool_config = {
    'feed_url': os.getenv('LIVERPOOL_FEED_URL'),
    'api_key': os.getenv('LIVERPOOL_API_KEY')
}
```

---

## 📊 Resumen de Estado

| Tienda | Método | Estado | Requiere |
|--------|--------|--------|----------|
| **Mercado Libre** | API Pública | ✅ Listo | Nada |
| **Amazon MX** | PA-API 5.0 | ⚠️ Requiere registro | Access Key, Secret Key, Partner Tag |
| **Walmart MX** | Feed/API Privada | ❌ No disponible | Contactar Walmart |
| **Liverpool** | Feed/API Privada | ❌ No disponible | Contactar Liverpool |
| **Coppel** | Feed JSON | ⚠️ Requiere URL | Feed URL |
| **Sears** | Feed XML | ⚠️ Requiere URL | Feed URL |

---

## 🚀 Siguientes Pasos

### Prioridad Alta:
1. ✅ **Mercado Libre** - Ya funcional, sin configuración necesaria
2. 🔐 **Amazon MX** - Registrarse en Associates y PA-API

### Prioridad Media:
3. 📞 **Walmart MX** - Contactar para feed o API
4. 📞 **Liverpool** - Contactar para feed o API
5. 📞 **Coppel** - Obtener URL de feed
6. 📞 **Sears** - Obtener URL de feed XML

---

## ❓ Troubleshooting

### Amazon PA-API Errors:

**Error: "Signature mismatch"**
- Verificar Access Key y Secret Key correctos
- Verificar formato de firma AWS Signature V4

**Error: "Not authorized"**
- Verificar que tienes 3 ventas calificadas
- Verificar que el Partner Tag es correcto

### Feed Errors:

**Error: "403 Forbidden"**
- URL del feed incorrecta
- Requiere autenticación adicional
- Feed no público

**Error: "JSON decode error"**
- Verificar formato del feed
- Verificar `product_path` correcto

---

## 📚 Referencias

- **Amazon PA-API:** https://webservices.amazon.com/paapi5/documentation/
- **Mercado Libre API:** https://developers.mercadolibre.com.mx/
- **Google Merchant Center:** https://support.google.com/merchants/

