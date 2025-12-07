# Frontend para MSPriceEngine - Requerimientos y Stack Tecnológico

## Resumen del Proyecto

Crear una **página web (frontend)** que consuma la API de MSPriceEngine para permitir a usuarios finales buscar y comparar precios de productos en tiendas mexicanas.

---

## 1. Objetivos del Frontend

### Objetivo Principal
Crear una interfaz web intuitiva y responsive que permita a usuarios buscar productos y comparar precios entre diferentes tiendas en México.

### Objetivos Secundarios
- Experiencia de usuario simple y rápida
- Diseño responsive (móvil y desktop)
- Visualización clara de precios y tiendas
- Performance optimizado (carga rápida)

---

## 2. Requerimientos Funcionales

### RF-01: Búsqueda de Productos
- Barra de búsqueda prominente en la página principal
- Búsqueda en tiempo real (opcional: sugerencias mientras escribe)
- Botón de búsqueda
- Validación mínima de 2 caracteres

### RF-02: Resultados de Búsqueda
- Mostrar lista de productos encontrados
- Información por producto:
  - Nombre del producto
  - Precio (formato: $12,999.99)
  - Tienda
  - Imagen (si está disponible)
  - Botón "Ver en tienda" (link al producto original)
- Ordenar por: Precio (menor a mayor / mayor a menor)
- Filtrar por: Tienda, Rango de precios

### RF-03: Paginación
- Mostrar 20 productos por página
- Botones: Anterior / Siguiente
- Indicador de página actual

### RF-04: Vista de Producto Individual
- Al hacer clic en un producto, mostrar detalles:
  - Nombre completo
  - Precio actual
  - Tienda
  - Imagen grande
  - SKU/ASIN
  - Última actualización
  - Link a la tienda original

### RF-05: Filtros (Opcional - Fase 2)
- Filtro por rango de precios (slider)
- Filtro por tiendas (checkboxes)
- Botón "Limpiar filtros"

### RF-06: Diseño Responsive
- Funcionar correctamente en:
  - Desktop (1920x1080, 1366x768)
  - Tablet (768x1024)
  - Móvil (375x667, 414x896)

---

## 3. Requerimientos No Funcionales

### RNF-01: Performance
- Tiempo de carga inicial: < 3 segundos
- Tiempo de búsqueda: < 1 segundo
- Imágenes optimizadas (lazy loading)

### RNF-02: Usabilidad
- Interfaz intuitiva (no requiere tutorial)
- Feedback visual en acciones (loading spinners)
- Mensajes de error claros

### RNF-03: Accesibilidad
- Contraste de colores adecuado
- Textos legibles (mínimo 14px)
- Navegación con teclado

### RNF-04: SEO (Opcional)
- Meta tags básicos
- URLs amigables
- Sitemap

---

## 4. Stack Tecnológico Recomendado

### Opción 1: React + Vite (RECOMENDADO)

**Stack:**
```
Frontend Framework: React 18+
Build Tool: Vite
UI Library: TailwindCSS
HTTP Client: Axios / Fetch API
State Management: React Hooks (useState, useEffect)
Routing: React Router DOM
Icons: Lucide React / React Icons
```

**Ventajas:**
- Rápido de desarrollar
- Vite es extremadamente rápido (HMR instantáneo)
- TailwindCSS = diseño rápido sin escribir CSS
- Comunidad enorme
- Fácil deployment (Vercel, Netlify)

**Estructura del proyecto:**
```
price-search-frontend/
├── src/
│   ├── components/
│   │   ├── SearchBar.jsx
│   │   ├── ProductCard.jsx
│   │   ├── ProductList.jsx
│   │   ├── Filters.jsx
│   │   └── Pagination.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── SearchResults.jsx
│   │   └── ProductDetail.jsx
│   ├── services/
│   │   └── api.js          # Axios client para API
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── package.json
└── vite.config.js
```

### Opción 2: Next.js (Si quieres SSR/SEO)

**Stack:**
```
Framework: Next.js 14+ (App Router)
Styling: TailwindCSS
HTTP Client: Fetch API (nativo)
```

**Ventajas:**
- SEO excelente (Server-Side Rendering)
- Image optimization automática
- API routes integradas
- Mejor para producción

**Desventajas:**
- Más complejo que React puro
- Curva de aprendizaje mayor

### Opción 3: HTML + Vanilla JavaScript (Minimalista)

**Stack:**
```
HTML5
CSS3 (o TailwindCSS CDN)
Vanilla JavaScript (ES6+)
Fetch API
```

**Ventajas:**
- Sin dependencias
- Cero configuración
- Muy ligero

**Desventajas:**
- Más código manual
- Menos features
- No recomendado para proyecto serio

---

## 5. Diseño de UI/UX (Wireframes en Texto)

### Página Principal (Home)

```
┌─────────────────────────────────────────────────────────┐
│  MSPriceEngine - Compara precios en México              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│               🔍 [Buscar producto...]  [Buscar]         │
│                                                         │
│  Busca entre miles de productos en Amazon, Walmart,    │
│  Liverpool y más tiendas mexicanas                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Página de Resultados

```
┌─────────────────────────────────────────────────────────┐
│  MSPriceEngine                          [Buscar...]     │
├─────────────────────────────────────────────────────────┤
│  Resultados para "laptop"  (15 productos)               │
│                                                         │
│  Filtros:                    Ordenar: [Precio ▼]       │
│  [ ] Amazon MX                                          │
│  [ ] Walmart MX              ┌──────────────────────┐   │
│  [ ] Liverpool               │ 📷                   │   │
│                              │ Laptop HP Pavilion   │   │
│  Precio: [______|______]     │ Gaming 15-dk1036la   │   │
│           $5k    $50k        │                      │   │
│                              │ $12,999.99           │   │
│                              │ Amazon MX            │   │
│                              │ [Ver en tienda]      │   │
│                              └──────────────────────┘   │
│                                                         │
│                              ┌──────────────────────┐   │
│                              │ 📷                   │   │
│                              │ Laptop Dell...       │   │
│                              │ $15,499.00           │   │
│                              │ Walmart MX           │   │
│                              └──────────────────────┘   │
│                                                         │
│                         [< Anterior] [Siguiente >]      │
└─────────────────────────────────────────────────────────┘
```

### Vista de Producto

```
┌─────────────────────────────────────────────────────────┐
│  MSPriceEngine                          [Buscar...]     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────────┐   Laptop HP Pavilion Gaming        │
│  │                │   15-dk1036la                       │
│  │   📷 Imagen    │                                     │
│  │    Grande      │   Precio: $12,999.99                │
│  │                │   Tienda: Amazon MX                 │
│  └────────────────┘   SKU: B08N5XQWB7                   │
│                       Actualizado: hace 2 horas         │
│                                                         │
│                       [🔗 Ver en Amazon MX]             │
│                                                         │
│                       Productos similares:              │
│                       ┌──────┐  ┌──────┐               │
│                       │ ... │  │ ... │               │
│                       └──────┘  └──────┘               │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Integración con API Backend

### Configuración de Axios (services/api.js)

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchProducts = async (query, filters = {}) => {
  const params = {
    q: query,
    ...filters,
  };
  const response = await api.get('/search', { params });
  return response.data;
};

export const getProduct = async (productId) => {
  const response = await api.get(`/products/${productId}`);
  return response.data;
};

export const getStores = async () => {
  const response = await api.get('/stores');
  return response.data;
};

export default api;
```

### Ejemplo de Uso en Componente

```javascript
import { useState, useEffect } from 'react';
import { searchProducts } from './services/api';

function SearchResults({ query }) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const data = await searchProducts(query);
        setProducts(data.products);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (query) {
      fetchProducts();
    }
  }, [query]);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

---

## 7. Paleta de Colores Sugerida

```css
/* Colores principales */
--primary: #3B82F6;      /* Azul - Botones principales */
--secondary: #10B981;    /* Verde - Precios */
--accent: #F59E0B;       /* Naranja - Destacados */

/* Neutrales */
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-800: #1F2937;
--gray-900: #111827;

/* Semánticos */
--success: #10B981;
--error: #EF4444;
--warning: #F59E0B;
```

---

## 8. Dependencias NPM (para React + Vite)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.300.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

---

## 9. Fases de Desarrollo del Frontend

### Fase 1: Setup y Estructura (1-2 días)
- [ ] Crear proyecto con Vite
- [ ] Configurar TailwindCSS
- [ ] Setup React Router
- [ ] Crear estructura de carpetas
- [ ] Configurar Axios

### Fase 2: Componentes Básicos (2-3 días)
- [ ] Componente SearchBar
- [ ] Componente ProductCard
- [ ] Componente ProductList
- [ ] Componente Pagination
- [ ] Layout principal

### Fase 3: Páginas (2-3 días)
- [ ] Página Home
- [ ] Página SearchResults
- [ ] Página ProductDetail
- [ ] Integración con API

### Fase 4: Funcionalidades Avanzadas (2-3 días)
- [ ] Filtros (precio, tiendas)
- [ ] Ordenamiento
- [ ] Loading states
- [ ] Error handling
- [ ] Responsive design

### Fase 5: Optimización y Deploy (1-2 días)
- [ ] Optimización de imágenes
- [ ] Performance tuning
- [ ] SEO básico
- [ ] Deploy a Vercel/Netlify

---

## 10. Comandos para Empezar

```bash
# Crear proyecto React con Vite
npm create vite@latest price-search-frontend -- --template react
cd price-search-frontend

# Instalar dependencias
npm install react-router-dom axios lucide-react

# Instalar TailwindCSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Iniciar desarrollo
npm run dev
```

---

## 11. Variables de Entorno

```env
# .env
VITE_API_URL=http://localhost:8000
```

```env
# .env.production
VITE_API_URL=https://api.mspriceengine.com
```

---

## 12. Deployment

### Opción 1: Vercel (Recomendado)
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Opción 2: Netlify
```bash
# Build
npm run build

# Deploy carpeta dist/ en Netlify UI
```

### Opción 3: GitHub Pages
```bash
# Configurar en vite.config.js
base: '/MSPriceEngine/'

# Build y deploy
npm run build
git subtree push --prefix dist origin gh-pages
```

---

## Resumen Final

### Stack Recomendado Final:
```
✓ React 18
✓ Vite
✓ TailwindCSS
✓ React Router DOM
✓ Axios
✓ Lucide React (iconos)
```

### Por qué este stack:
- **Rápido**: Vite HMR instantáneo
- **Simple**: No over-engineering
- **Moderno**: React 18 + hooks
- **Bonito**: TailwindCSS para diseño rápido
- **Deployable**: Un comando → producción

### Tiempo estimado de desarrollo:
- **MVP básico**: 1 semana
- **Con filtros y features**: 2 semanas
- **Pulido y production-ready**: 3 semanas

---

**Listo para empezar?** El siguiente paso es:
```bash
npm create vite@latest price-search-frontend -- --template react
```
