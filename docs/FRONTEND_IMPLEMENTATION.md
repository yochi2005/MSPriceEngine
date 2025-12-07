# Frontend Implementation - MSPriceEngine

## Ubicación del Proyecto

```
/home/yochi/Documents/mspriceengine-frontend/
```

## Stack Tecnológico Implementado

✅ **React 18** - Framework principal
✅ **Vite 6** - Build tool y dev server
✅ **TailwindCSS 3** - Estilos y diseño responsivo
✅ **Lucide React** - Iconos modernos

## Estructura del Proyecto

```
mspriceengine-frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx         # Barra superior sticky con búsqueda
│   │   ├── SearchHero.jsx     # Hero section con búsqueda principal
│   │   ├── ProductCard.jsx    # Card individual de producto
│   │   └── ProductGrid.jsx    # Grid de productos con estados
│   ├── services/
│   │   └── api.js             # Servicio de API para backend
│   ├── App.jsx                # Componente principal
│   ├── main.jsx              # Entry point
│   └── index.css             # Estilos globales + Tailwind
├── public/                    # Archivos estáticos
├── .env                      # Variables de entorno
├── tailwind.config.js        # Configuración de Tailwind
├── postcss.config.js         # Configuración de PostCSS
├── vite.config.js            # Configuración de Vite
├── package.json              # Dependencias npm
└── README.md                 # Documentación del frontend
```

## Componentes Creados

### 1. Header.jsx
**Función:** Barra superior sticky con búsqueda

**Features:**
- Sticky al hacer scroll
- Logo "MSPriceEngine" en azul
- Búsqueda integrada en desktop
- Búsqueda colapsable en mobile
- Responsive (oculta/muestra elementos según tamaño)

**Props:**
- `onSearch` - Función para ejecutar búsqueda
- `searchQuery` - Query actual
- `setSearchQuery` - Función para actualizar query

### 2. SearchHero.jsx
**Función:** Hero section con búsqueda principal y sugerencias

**Features:**
- Gradiente de fondo azul suave
- Input grande para búsqueda
- Botón "Buscar" destacado
- Búsquedas populares sugeridas (iPhone, Laptop, Audífonos)
- Se oculta después de la primera búsqueda

**Props:**
- `onSearch` - Función para ejecutar búsqueda
- `searchQuery` - Query actual
- `setSearchQuery` - Función para actualizar query

### 3. ProductCard.jsx
**Función:** Card individual para mostrar producto

**Features:**
- Imagen del producto (aspect ratio 16:9)
- Nombre truncado a 2 líneas
- Precio formateado en MXN
- Nombre de la tienda con icono
- Botón "Ver producto" que abre URL externa
- Hover effect (elevación y sombra)
- Fallback de imagen (emoji 📦)

**Props:**
- `product` - Objeto con datos del producto

**Estructura del producto:**
```javascript
{
  id: number,
  name: string,
  price: number,
  store_url: string,
  image_url: string,
  store: {
    name: string
  }
}
```

### 4. ProductGrid.jsx
**Función:** Grid responsivo de productos con estados

**Features:**
- Loading state con spinner
- Error state con botón de retry
- Empty state con mensaje
- Grid responsivo (1, 2, 3, 4 columnas)
- Contador de resultados

**Props:**
- `products` - Array de productos
- `loading` - Boolean de carga
- `error` - String de error
- `searchTerm` - Término buscado

## Servicio de API (api.js)

### Métodos Disponibles

```javascript
// Buscar productos
apiService.searchProducts(query, filters)
// Returns: { total: number, products: Product[] }

// Obtener producto específico
apiService.getProduct(id)
// Returns: Product

// Obtener tiendas
apiService.getStores()
// Returns: Store[]

// Health check del API
apiService.healthCheck()
// Returns: boolean
```

### Configuración

URL del API se configura en `.env`:
```env
VITE_API_URL=http://localhost:8000
```

## Diseño Visual Implementado

### Paleta de Colores

```css
Primary: #2563eb (Azul)
Primary Hover: #1d4ed8
Primary Light: #dbeafe
Background: #f9fafb (Gris muy claro)
White: #ffffff
Text Primary: #111827
Text Secondary: #6b7280
Border: #e5e7eb
```

### Tipografía

- **Fuente:** Inter (Google Fonts)
- **Tamaños:**
  - H1 Hero: 3xl-5xl (responsive)
  - Product Title: lg (18px)
  - Price: 2xl (24px)
  - Body: base (16px)
  - Small: sm (14px)

### Grid Responsivo

```css
Mobile (< 640px):     1 columna
Tablet (640-1023px):  2 columnas
Desktop (1024-1279px): 3 columnas
Large Desktop (1280px+): 4 columnas
```

### Espaciado

- Padding cards: 16px
- Gap entre cards: 24px (desktop), 16px (mobile)
- Max width contenedor: 1280px
- Márgenes sección: 32px

## Estados de la UI

### 1. Estado Inicial (Hero)
- Muestra hero section con búsqueda grande
- No muestra productos
- Sugerencias de búsqueda

### 2. Estado de Carga (Loading)
- Spinner animado
- Mensaje "Buscando productos..."
- Hero oculto

### 3. Estado con Resultados
- Hero oculto
- Contador de resultados
- Grid de productos
- Hover effects en cards

### 4. Estado Vacío (Empty)
- Icono de búsqueda 🔍
- Mensaje "No encontramos resultados"
- Sugerencia para buscar de nuevo

### 5. Estado de Error
- Icono de advertencia ⚠️
- Mensaje de error
- Botón "Intentar de nuevo"

## Características Implementadas

✅ **Responsive Design**
- Mobile first approach
- Breakpoints: 640px, 768px, 1024px, 1280px
- Grid adaptable
- Header colapsable

✅ **Integración con API**
- Conexión a backend FastAPI
- Health check automático
- Manejo de errores
- Loading states

✅ **UX/UI**
- Transiciones suaves
- Hover effects
- Focus states
- Animaciones sutiles

✅ **Accesibilidad**
- Alto contraste
- Botones touch-friendly
- Links externos con `rel="noopener noreferrer"`
- Fallbacks para imágenes

✅ **Performance**
- Code splitting automático (Vite)
- Lazy loading de componentes
- Optimización de imágenes
- Tree-shaking de TailwindCSS

## Cómo Usar

### Desarrollo Local

```bash
# 1. Ir al directorio
cd /home/yochi/Documents/mspriceengine-frontend

# 2. Instalar dependencias (ya hecho)
npm install

# 3. Iniciar dev server
npm run dev

# 4. Abrir en navegador
http://localhost:5173
```

### Probar con Backend

```bash
# Terminal 1 - Backend API
cd /home/yochi/Documents/MSPriceEngine
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd /home/yochi/Documents/mspriceengine-frontend
npm run dev

# Visitar http://localhost:5173
```

### Build para Producción

```bash
cd /home/yochi/Documents/mspriceengine-frontend
npm run build

# Output en: dist/
```

## Dependencias Instaladas

```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.468.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^7.2.6",
    "tailwindcss": "^3.4.17",
    "postcss": "^8.5.1",
    "autoprefixer": "^10.4.20"
  }
}
```

## Próximos Pasos

### Mejoras Pendientes

1. **Filtros de Búsqueda**
   - Por rango de precio
   - Por tienda
   - Por disponibilidad

2. **Paginación**
   - Implementar botones anterior/siguiente
   - Mostrar número de página
   - Lazy loading infinito (opcional)

3. **Ordenamiento**
   - Por precio (menor a mayor, mayor a menor)
   - Por relevancia
   - Por fecha de actualización

4. **Vista de Detalle**
   - Modal o página de producto individual
   - Historial de precios (gráfico)
   - Comparación directa

5. **Favoritos**
   - Guardar productos en localStorage
   - Lista de seguimiento de precios
   - Notificaciones (futuro)

6. **Mejoras UX**
   - Skeleton loading (en lugar de spinner)
   - Animaciones de entrada de cards
   - Búsqueda con autocompletado
   - Historial de búsquedas

## Deployment

### Cloudflare Pages (Recomendado)

1. **Subir a GitHub**
```bash
cd /home/yochi/Documents/mspriceengine-frontend
git init
git add .
git commit -m "Initial frontend implementation"
git remote add origin git@github.com:yochi2005/mspriceengine-frontend.git
git push -u origin main
```

2. **Configurar en Cloudflare**
   - Ir a dash.cloudflare.com
   - Pages → Create project
   - Connect GitHub repo: `mspriceengine-frontend`
   - Build settings:
     - Build command: `npm run build`
     - Output directory: `dist`
     - Environment variable: `VITE_API_URL=https://your-backend-url.railway.app`

3. **Deploy**
   - Automático en cada push a main
   - URL: `mspriceengine-frontend.pages.dev`

### Vercel (Alternativa)

```bash
npm install -g vercel
cd /home/yochi/Documents/mspriceengine-frontend
vercel
```

## URLs Finales

### Desarrollo
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Producción (Futuro)
- Frontend: https://mspriceengine-frontend.pages.dev
- Backend: https://mspriceengine.up.railway.app
- Custom domain (opcional): https://mspriceengine.com

## Archivos de Configuración

### tailwind.config.js
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb',
          hover: '#1d4ed8',
          light: '#dbeafe',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
}
```

### .env
```env
VITE_API_URL=http://localhost:8000
```

### vite.config.js (Default)
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

## Testing

```bash
# Probar búsqueda
1. Ir a http://localhost:5173
2. Escribir "laptop" en buscador
3. Presionar Enter o clic en "Buscar"
4. Verificar que aparezcan productos (si hay en BD)

# Probar estados
- Empty: Buscar "asdfasdf" (sin resultados)
- Loading: Hacer búsqueda rápida
- Error: Apagar backend API y buscar
```

## Troubleshooting

### Error: API not responding
**Solución:** Verificar que backend esté corriendo en puerto 8000

### Error: CORS
**Solución:** Backend ya tiene CORS habilitado para localhost:5173

### Error: Images not loading
**Solución:** Normal si no hay URLs de imágenes en BD, se muestra emoji 📦

### Estilos no aparecen
**Solución:**
```bash
npm install -D tailwindcss postcss autoprefixer
```

---

**Fecha:** 7 de diciembre de 2024
**Versión:** 1.0
**Estado:** ✅ Implementado y funcionando
