# Guía: Cómo Agregar Productos a Magic Solutions Price API

Esta guía explica paso a paso cómo agregar productos a la base de datos de MSPriceEngine.

---

## Tabla de Contenidos

1. [Métodos para Agregar Productos](#métodos-para-agregar-productos)
2. [Método 1: Editar populate_db.py](#método-1-editar-populate_dbpy)
3. [Método 2: Usar el Endpoint de Carga Masiva](#método-2-usar-el-endpoint-de-carga-masiva)
4. [Método 3: Script Python Personalizado](#método-3-script-python-personalizado)
5. [IDs de Referencia](#ids-de-referencia)
6. [Consejos y Mejores Prácticas](#consejos-y-mejores-prácticas)
7. [Solución de Problemas](#solución-de-problemas)

---

## Métodos para Agregar Productos

Existen **3 métodos principales** para agregar productos:

1. **Editar `populate_db.py`** - Mejor para agregar muchos productos de una vez
2. **Usar el endpoint `/products/bulk`** - Mejor para integraciones y automatización
3. **Script Python personalizado** - Mejor para casos específicos

---

## Método 1: Editar populate_db.py

**Este es el método MÁS FÁCIL y RECOMENDADO** para agregar productos manualmente.

### Paso 1: Abrir el archivo

```bash
cd ~/Documents/MSPriceEngine
nano populate_db.py
# o usa tu editor preferido:
code populate_db.py
```

### Paso 2: Localizar la sección de productos

Busca la lista `products_data` (aproximadamente línea 50-160):

```python
products_data = [
    # Laptops
    {"name": "MacBook Air M2 13 pulgadas", "category": "laptops", ...},
    {"name": "Dell XPS 15", "category": "laptops", ...},
    # ... más productos
]
```

### Paso 3: Agregar tus productos

Agrega nuevos productos siguiendo esta estructura:

```python
{
    "name": "Nombre del Producto",           # REQUERIDO
    "category": "slug-categoria",            # REQUERIDO (ver lista abajo)
    "store": "Nombre de la Tienda",          # REQUERIDO (ver lista abajo)
    "price": 12999.00,                       # REQUERIDO (float)
    "url": "https://tienda.com/producto",    # REQUERIDO
    "image": "https://imagen.com/img.jpg"    # REQUERIDO
}
```

#### Ejemplo Real - Agregar un nuevo iPhone:

```python
# Dentro de la sección # Smartphones
{
    "name": "iPhone 14 128GB",
    "category": "smartphones",
    "store": "Amazon MX",
    "price": 19999.00,
    "url": "https://amazon.com.mx/iphone-14",
    "image": "https://m.media-amazon.com/images/I/61bK6PMOC3L._AC_SL1500_.jpg"
}
```

#### Ejemplo - Agregar una Laptop Gaming:

```python
# Dentro de la sección # Laptops
{
    "name": "MSI GF63 Thin Intel Core i5",
    "category": "laptops",
    "store": "Mercado Libre",
    "price": 15999.00,
    "url": "https://mercadolibre.com.mx/msi-gf63",
    "image": "https://http2.mlstatic.com/D_NQ_NP_12345-MLM.jpg"
}
```

### Paso 4: Guardar y ejecutar el script

```bash
# Guardar el archivo (Ctrl+O en nano, Ctrl+S en VSCode)

# Ejecutar el script
cd ~/Documents/MSPriceEngine
source venv/bin/activate
python populate_db.py
```

**IMPORTANTE:** Este script **eliminará todos los productos existentes** y recreará la base de datos desde cero.

### Paso 5: Verificar los productos

```bash
# Verificar en la API
curl "http://localhost:8000/search?q=MSI"

# O visitar el navegador
http://localhost:5174
```

---

## Método 2: Usar el Endpoint de Carga Masiva

**Mejor para:** Agregar productos sin borrar los existentes, integraciones, automatización.

### Paso 1: Preparar el archivo JSON

Crea un archivo `nuevos_productos.json`:

```json
{
  "products": [
    {
      "name": "iPhone 14 128GB",
      "store_id": 1,
      "category_id": 2,
      "store_url": "https://amazon.com.mx/iphone-14",
      "price": 19999.00,
      "image_url": "https://m.media-amazon.com/images/I/61bK6PMOC3L._AC_SL1500_.jpg",
      "currency": "MXN",
      "available": 1
    },
    {
      "name": "Samsung Galaxy A54",
      "store_id": 2,
      "category_id": 2,
      "store_url": "https://walmart.com.mx/galaxy-a54",
      "price": 8999.00,
      "image_url": "https://m.media-amazon.com/images/I/71vFKBpKakL._AC_SL1500_.jpg",
      "currency": "MXN",
      "available": 1
    }
  ]
}
```

### Paso 2: Enviar la petición al API

```bash
curl -X POST http://localhost:8000/products/bulk \
  -H "Content-Type: application/json" \
  -d @nuevos_productos.json
```

**Respuesta exitosa:**
```json
{
  "created": 2,
  "failed": 0,
  "errors": []
}
```

### Paso 3: Verificar

```bash
curl "http://localhost:8000/search?q=Samsung"
```

---

## Método 3: Script Python Personalizado

**Mejor para:** Agregar productos programáticamente, migraciones, sincronización.

### Crear archivo: `add_products.py`

```python
"""
Script para agregar productos a la base de datos sin borrar los existentes
"""
from app.database import SessionLocal
from app import models

def add_products():
    db = SessionLocal()

    try:
        # Definir los nuevos productos
        new_products = [
            {
                "name": "iPhone 14 128GB",
                "store_id": 1,  # Amazon MX
                "category_id": 2,  # Smartphones
                "store_url": "https://amazon.com.mx/iphone-14",
                "price": 19999.00,
                "image_url": "https://m.media-amazon.com/images/I/61bK6PMOC3L._AC_SL1500_.jpg",
                "currency": "MXN",
                "available": 1
            },
            {
                "name": "Samsung Galaxy A54",
                "store_id": 2,  # Walmart MX
                "category_id": 2,  # Smartphones
                "store_url": "https://walmart.com.mx/galaxy-a54",
                "price": 8999.00,
                "image_url": "https://m.media-amazon.com/images/I/71vFKBpKakL._AC_SL1500_.jpg",
                "currency": "MXN",
                "available": 1
            }
        ]

        # Insertar productos
        created_count = 0
        for product_data in new_products:
            product = models.Product(**product_data)
            db.add(product)
            created_count += 1

        db.commit()

        print(f"✅ {created_count} productos agregados exitosamente!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_products()
```

### Ejecutar el script

```bash
cd ~/Documents/MSPriceEngine
source venv/bin/activate
python add_products.py
```

---

## IDs de Referencia

### Tiendas (store_id)

| ID | Nombre | Slug |
|----|--------|------|
| 1 | Amazon MX | `"Amazon MX"` |
| 2 | Walmart MX | `"Walmart MX"` |
| 3 | Liverpool | `"Liverpool"` |
| 4 | Mercado Libre | `"Mercado Libre"` |
| 5 | Coppel | `"Coppel"` |
| 6 | Elektra | `"Elektra"` |

**Consultar tiendas:**
```bash
curl http://localhost:8000/stores
```

### Categorías (category_id)

| ID | Nombre | Slug | Descripción |
|----|--------|------|-------------|
| 1 | Laptops | `"laptops"` | Laptops y computadoras portátiles |
| 2 | Smartphones | `"smartphones"` | Teléfonos inteligentes |
| 3 | Tablets | `"tablets"` | Tabletas electrónicas |
| 4 | Audio | `"audio"` | Audífonos, bocinas y audio |
| 5 | TV y Video | `"tv-video"` | Televisores y dispositivos de video |
| 6 | Gaming | `"gaming"` | Consolas y videojuegos |
| 7 | Smartwatches | `"smartwatches"` | Relojes inteligentes |
| 8 | Cámaras | `"camaras"` | Cámaras fotográficas y accesorios |

**Consultar categorías:**
```bash
curl http://localhost:8000/categories
```

---

## Consejos y Mejores Prácticas

### 1. Imágenes de Productos

**Recomendaciones:**
- Usar imágenes de alta calidad (min 800x800px)
- Preferir URLs de CDN (Amazon, Cloudinary, etc.)
- Verificar que las URLs sean accesibles públicamente

**Fuentes recomendadas de imágenes:**
- Amazon CDN: `https://m.media-amazon.com/images/I/`
- Walmart: `https://i5.walmartimages.com/`
- Liverpool: `https://ss[X].liverpool.com.mx/`

**Ejemplo de URL válida:**
```
https://m.media-amazon.com/images/I/71jG+e7roXL._AC_SL1500_.jpg
```

### 2. Nombres de Productos

**✅ BUENO:**
```
"MacBook Air M2 13 pulgadas 256GB"
"iPhone 15 Pro Max 256GB Titanio Negro"
"Samsung Galaxy S24 Ultra 5G 12GB RAM"
```

**❌ EVITAR:**
```
"¡¡¡OFERTA!!! MacBook Air M2 $$$ SUPER PRECIO $$$"
"iphone 15 pro max"  (sin detalles)
"SAMSUNG GALAXY S24 ULTRA" (todo mayúsculas)
```

### 3. Precios

- Usar precios **reales y actuales**
- Formato: `19999.00` (float con 2 decimales)
- Moneda: Siempre `"MXN"` para México

### 4. URLs de Productos

**Formato correcto:**
```
https://www.amazon.com.mx/dp/B0ABCDEFGH
https://www.walmart.com.mx/producto/12345678
https://www.liverpool.com.mx/tienda/producto
```

**Evitar:**
- URLs con parámetros de tracking largos
- URLs cortas/temporales
- URLs que requieren login

### 5. Disponibilidad

- `available: 1` = Producto disponible
- `available: 0` = Producto agotado

---

## Solución de Problemas

### Error: "Store ID not found"

**Problema:** El `store_id` no existe en la base de datos.

**Solución:**
```bash
# Verificar IDs disponibles
curl http://localhost:8000/stores

# Usar el ID correcto (1-6)
```

### Error: "Category ID not found"

**Problema:** El `category_id` no existe.

**Solución:**
```bash
# Verificar IDs disponibles
curl http://localhost:8000/categories

# Usar el ID correcto (1-8)
```

### Error: "Integrity error"

**Problema:** Puede deberse a:
- Producto duplicado
- Constraint violation

**Solución:**
```python
# Asegúrate que el producto no exista
# Verifica que todos los campos requeridos estén presentes
```

### Las imágenes no se muestran

**Problema:** URL de imagen inválida o inaccesible.

**Solución:**
1. Verifica que la URL sea accesible en el navegador
2. Asegúrate que no requiera autenticación
3. Usa URLs de CDN públicos

**Prueba la URL:**
```bash
curl -I "https://m.media-amazon.com/images/I/71jG+e7roXL._AC_SL1500_.jpg"
# Debe retornar: HTTP/1.1 200 OK
```

---

## Ejemplos Completos

### Ejemplo 1: Agregar Consolas de Videojuegos

```python
# En populate_db.py, sección # Gaming
{
    "name": "PlayStation 5 Slim Digital Edition",
    "category": "gaming",
    "store": "Amazon MX",
    "price": 11999.00,
    "url": "https://amazon.com.mx/ps5-slim-digital",
    "image": "https://m.media-amazon.com/images/I/51DKubiQEyL._AC_SL1001_.jpg"
},
{
    "name": "Steam Deck 512GB",
    "category": "gaming",
    "store": "Mercado Libre",
    "price": 16999.00,
    "url": "https://mercadolibre.com.mx/steam-deck-512gb",
    "image": "https://m.media-amazon.com/images/I/71y5XKRl5iL._AC_SL1500_.jpg"
}
```

### Ejemplo 2: Agregar Accesorios de Audio

```python
# En populate_db.py, sección # Audio
{
    "name": "Marshall Emberton II Bluetooth Speaker",
    "category": "audio",
    "store": "Liverpool",
    "price": 4999.00,
    "url": "https://liverpool.com.mx/marshall-emberton-ii",
    "image": "https://m.media-amazon.com/images/I/61RQP8GTGGL._AC_SL1500_.jpg"
},
{
    "name": "Sennheiser Momentum 4 Wireless",
    "category": "audio",
    "store": "Amazon MX",
    "price": 8999.00,
    "url": "https://amazon.com.mx/sennheiser-momentum-4",
    "image": "https://m.media-amazon.com/images/I/51p7wCPT4WL._AC_SL1500_.jpg"
}
```

### Ejemplo 3: Agregar Productos de Diferentes Tiendas

```python
# Mismo producto en diferentes tiendas para comparar precios
{
    "name": "AirPods Pro 2da Generación",
    "category": "audio",
    "store": "Amazon MX",
    "price": 5999.00,
    "url": "https://amazon.com.mx/airpods-pro-2",
    "image": "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg"
},
{
    "name": "AirPods Pro 2da Generación",
    "category": "audio",
    "store": "Liverpool",
    "price": 6199.00,
    "url": "https://liverpool.com.mx/airpods-pro-2",
    "image": "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg"
},
{
    "name": "AirPods Pro 2da Generación",
    "category": "audio",
    "store": "Coppel",
    "price": 6299.00,
    "url": "https://coppel.com/airpods-pro-2",
    "image": "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg"
}
```

---

## Workflow Recomendado

### Para agregar 1-10 productos:

1. Editar `populate_db.py`
2. Agregar productos en la sección correspondiente
3. Ejecutar script
4. Verificar en la API/Frontend

### Para agregar 10-100 productos:

1. Crear archivo JSON con los productos
2. Usar endpoint `/products/bulk`
3. Verificar respuesta
4. Revisar errores si los hay

### Para agregar 100+ productos:

1. Crear script Python personalizado
2. Implementar manejo de errores robusto
3. Agregar en lotes de 50-100
4. Implementar reintentos para errores

---

## Comandos Útiles

```bash
# Ver todos los productos
curl "http://localhost:8000/search?q=&per_page=100"

# Ver productos por categoría
curl "http://localhost:8000/categories/1/products"

# Ver productos por tienda
curl "http://localhost:8000/stores/1/products"

# Contar productos totales
curl "http://localhost:8000/search?q=&per_page=1" | python3 -m json.tool | grep total

# Reiniciar base de datos desde cero
cd ~/Documents/MSPriceEngine
rm -f mspriceengine.db
python populate_db.py
```

---

## Próximos Pasos

Una vez que domines agregar productos manualmente, puedes:

1. **Crear scrapers** para automatizar la obtención de productos
2. **Implementar actualización de precios** automática
3. **Agregar validación de URLs** para verificar disponibilidad
4. **Implementar sistema de alertas** cuando cambien precios
5. **Crear dashboard** para gestión de productos

---

## Soporte

Si encuentras problemas:

1. Revisa los logs del servidor:
   ```bash
   # Ver logs de la API
   tail -f /tmp/api_log.txt
   ```

2. Verifica la estructura de la base de datos:
   ```bash
   sqlite3 ~/Documents/MSPriceEngine/mspriceengine.db
   .schema products
   .quit
   ```

3. Consulta la documentación completa:
   - `docs/BACKEND_IMPROVEMENTS.md`
   - `docs/API.md`
   - Swagger UI: http://localhost:8000/docs

---

**Última actualización:** 8 de Diciembre, 2025
**Versión de la API:** 0.2.0
