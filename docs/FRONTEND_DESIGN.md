# Diseño Visual Frontend - MSPriceEngine

## 1. Layout General

### Desktop (1024px+)
```
┌─────────────────────────────────────────────────────────────┐
│                        HEADER                                │
│  [Logo MSPriceEngine]              [Buscar productos...]  🔍 │
└─────────────────────────────────────────────────────────────┘
│                                                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │     [Input grande de búsqueda]           [Buscar]     │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                               │
│  Encontrados 24 resultados para "laptop"                      │
│                                                               │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐             │
│  │ Card 1 │  │ Card 2 │  │ Card 3 │  │ Card 4 │             │
│  │        │  │        │  │        │  │        │             │
│  └────────┘  └────────┘  └────────┘  └────────┘             │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐             │
│  │ Card 5 │  │ Card 6 │  │ Card 7 │  │ Card 8 │             │
│  │        │  │        │  │        │  │        │             │
│  └────────┘  └────────┘  └────────┘  └────────┘             │
│                                                               │
│               [← Anterior] [1] [2] [3] [Siguiente →]         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Tablet (768px - 1023px)
```
┌─────────────────────────────────────┐
│          HEADER                      │
│  [Logo]      [Buscar...]  🔍         │
└─────────────────────────────────────┘
│                                      │
│  ┌──────────────────────────────┐   │
│  │  [Input]        [Buscar]     │   │
│  └──────────────────────────────┘   │
│                                      │
│  24 resultados                       │
│                                      │
│  ┌─────────┐  ┌─────────┐           │
│  │ Card 1  │  │ Card 2  │           │
│  └─────────┘  └─────────┘           │
│  ┌─────────┐  ┌─────────┐           │
│  │ Card 3  │  │ Card 4  │           │
│  └─────────┘  └─────────┘           │
│                                      │
└─────────────────────────────────────┘
```

### Mobile (< 768px)
```
┌──────────────────────┐
│      HEADER          │
│  [MSPrice]     🔍    │
└──────────────────────┘
│                      │
│  ┌────────────────┐  │
│  │ [Buscar...]    │  │
│  └────────────────┘  │
│                      │
│  24 resultados       │
│                      │
│  ┌────────────────┐  │
│  │    Card 1      │  │
│  │                │  │
│  └────────────────┘  │
│  ┌────────────────┐  │
│  │    Card 2      │  │
│  │                │  │
│  └────────────────┘  │
│                      │
└──────────────────────┘
```

---

## 2. Paleta de Colores

### Colores Principales
```css
/* Azul primario - confianza, tecnología */
--primary: #2563eb;        /* Blue 600 */
--primary-hover: #1d4ed8;  /* Blue 700 */
--primary-light: #dbeafe; /* Blue 100 */

/* Grises - neutrales, profesional */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-900: #111827;

/* Fondo y texto */
--bg-primary: #ffffff;
--bg-secondary: #f9fafb;
--text-primary: #111827;
--text-secondary: #6b7280;

/* Acentos */
--success: #10b981;  /* Verde para precios buenos */
--warning: #f59e0b;  /* Amarillo para stock limitado */
--border: #e5e7eb;
```

### Aplicación
- **Fondo página**: Gris muy claro (#f9fafb)
- **Cards**: Blanco puro (#ffffff)
- **Botones primarios**: Azul (#2563eb)
- **Texto principal**: Gris oscuro (#111827)
- **Texto secundario**: Gris medio (#6b7280)
- **Bordes**: Gris claro (#e5e7eb)

---

## 3. Tipografía

### Fuente Recomendada
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Inter** - Fuente moderna, legible, gratis de Google Fonts

### Jerarquía Tipográfica
```css
/* Logo / Títulos principales */
.text-2xl { font-size: 24px; font-weight: 700; }

/* Títulos de producto */
.text-lg { font-size: 18px; font-weight: 600; }

/* Precios */
.text-xl { font-size: 20px; font-weight: 700; }

/* Texto normal */
.text-base { font-size: 16px; font-weight: 400; }

/* Texto pequeño (tienda, metadatos) */
.text-sm { font-size: 14px; font-weight: 400; }

/* Texto muy pequeño */
.text-xs { font-size: 12px; font-weight: 400; }
```

---

## 4. Componentes Visuales

### 4.1 Header / Barra Superior
```
┌─────────────────────────────────────────────────────────┐
│  [Logo MSPriceEngine]                    [Buscar...]  🔍│
└─────────────────────────────────────────────────────────┘
```

**Especificaciones:**
- Altura: 64px
- Fondo: Blanco con sombra suave
- Logo: Texto azul bold "MSPriceEngine"
- Buscador: Input con icono de búsqueda
- Sticky al hacer scroll

**Código visual:**
```css
height: 64px;
background: white;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
padding: 0 24px;
position: sticky;
top: 0;
z-index: 50;
```

---

### 4.2 Input de Búsqueda Principal
```
┌────────────────────────────────────────────────────┐
│  🔍  Busca productos en Amazon, Walmart...   [Buscar] │
└────────────────────────────────────────────────────┘
```

**Especificaciones:**
- Ancho: 100% (max 800px centrado)
- Altura: 56px
- Borde redondeado: 12px
- Sombra sutil
- Placeholder gris claro
- Icono de lupa a la izquierda
- Botón azul a la derecha

**Estados:**
- Normal: Borde gris claro
- Focus: Borde azul, sombra azul
- Hover: Borde gris medio

---

### 4.3 Card de Producto
```
┌─────────────────────────────┐
│  ┌───────────────────────┐  │
│  │                       │  │ ← Imagen (16:9)
│  │      [Imagen]         │  │
│  │                       │  │
│  └───────────────────────┘  │
│                             │
│  Laptop HP 15.6" Intel...  │ ← Título (2 líneas max)
│                             │
│  $12,999.00                 │ ← Precio (grande, bold)
│  MXN                        │
│                             │
│  🏪 Amazon MX               │ ← Tienda
│                             │
│  [Ver producto →]           │ ← Botón
└─────────────────────────────┘
```

**Especificaciones:**
- Ancho: Flex (responsive)
- Fondo: Blanco
- Borde: 1px gris claro
- Esquinas: 12px redondeadas
- Padding: 16px
- Sombra hover: Elevación suave
- Transición suave al hover

**CSS:**
```css
background: white;
border: 1px solid #e5e7eb;
border-radius: 12px;
padding: 16px;
transition: all 0.2s ease;

/* Hover */
:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}
```

**Elementos internos:**
- **Imagen**: Aspect ratio 16:9, object-fit cover
- **Título**: 2 líneas máximo con ellipsis
- **Precio**: Color azul, bold, 24px
- **Tienda**: Gris medio, 14px, con emoji
- **Botón**: Azul, ancho completo, hover más oscuro

---

### 4.4 Grid de Resultados

**Desktop (4 columnas):**
```css
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 24px;
```

**Tablet (2 columnas):**
```css
@media (max-width: 1023px) {
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
```

**Mobile (1 columna):**
```css
@media (max-width: 767px) {
  grid-template-columns: 1fr;
  gap: 16px;
}
```

---

### 4.5 Botón "Ver Producto"
```
┌────────────────────┐
│  Ver producto  →   │
└────────────────────┘
```

**Especificaciones:**
- Ancho: 100%
- Altura: 40px
- Fondo: Azul primario
- Texto: Blanco, 14px, medium
- Borde: Ninguno
- Esquinas: 8px
- Hover: Azul más oscuro + cursor pointer

---

## 5. Responsividad

### Breakpoints
```css
/* Mobile first */
/* Pequeño (default) */
< 640px  → 1 columna

/* Tablet */
640px - 767px  → 2 columnas (opcional)
768px - 1023px → 2 columnas

/* Desktop */
1024px - 1279px → 3 columnas
1280px+         → 4 columnas
```

### Adaptaciones por Tamaño

#### Mobile (< 768px)
- Header: Logo pequeño + icono búsqueda
- Input: Ancho completo, más grande (touch friendly)
- Grid: 1 columna
- Padding: 16px
- Tarjetas: Ancho completo
- Imagen producto: Más pequeña (ratio 4:3)

#### Tablet (768px - 1023px)
- Header: Logo mediano + búsqueda compacta
- Grid: 2 columnas
- Padding: 24px
- Tarjetas: Más cuadradas

#### Desktop (1024px+)
- Header: Full con búsqueda integrada
- Grid: 4 columnas
- Padding: 32px
- Max width: 1280px centrado
- Hover effects más visibles

---

## 6. Espaciado y Jerarquía

### Sistema de Espaciado (Tailwind)
```css
/* Spacing scale */
4px   → spacing-1  (gap mínimo)
8px   → spacing-2  (texto-icono)
12px  → spacing-3  (elementos cercanos)
16px  → spacing-4  (padding cards)
24px  → spacing-6  (gap grid)
32px  → spacing-8  (secciones)
48px  → spacing-12 (márgenes grandes)
```

### Jerarquía Visual

**1. Input de búsqueda** (más importante)
- Posición central
- Tamaño grande
- Color destacado

**2. Resultados de productos**
- Grid organizado
- Cards limpias
- Precio destacado

**3. Header**
- Discreto pero presente
- Sticky para acceso rápido

---

## 7. Estilo Visual General

### Principios de Diseño

1. **Minimalista**
   - Mucho espacio en blanco
   - Sin decoraciones innecesarias
   - Jerarquía clara

2. **Enfoque en Resultados**
   - Cards simples
   - Información esencial visible
   - Precio destacado

3. **Moderno**
   - Bordes redondeados (12px)
   - Sombras suaves
   - Transiciones fluidas
   - Tipografía limpia

4. **Accesible**
   - Alto contraste texto/fondo
   - Botones grandes (touch friendly)
   - Focus states visibles

---

## 8. Ejemplo Visual Completo

### Hero Section (Búsqueda principal)
```
┌─────────────────────────────────────────────────────────┐
│                                                           │
│              Encuentra los mejores precios                │
│           Compara productos de las mejores tiendas        │
│                                                           │
│  ┌───────────────────────────────────────────────────┐   │
│  │ 🔍  Busca iPhone, laptop, audífonos...  [Buscar] │   │
│  └───────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```
- Fondo: Gradiente suave azul claro
- Texto: Centro, grande
- Input: Destacado, sombra

### Resultados Section
```
┌─────────────────────────────────────────────────────────┐
│  Encontrados 24 resultados para "laptop"                 │
│                                                           │
│  [Filtros: Precio  Tienda  Disponibilidad]              │
│                                                           │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐                 │
│  │      │  │      │  │      │  │      │                 │
│  │ Card │  │ Card │  │ Card │  │ Card │                 │
│  │      │  │      │  │      │  │      │                 │
│  └──────┘  └──────┘  └──────┘  └──────┘                 │
│                                                           │
└─────────────────────────────────────────────────────────┘
```
- Fondo: Gris muy claro
- Cards: Blanco con hover
- Gap: 24px entre cards

---

## 9. Animaciones y Transiciones

### Micro-interacciones
```css
/* Hover en cards */
transition: transform 0.2s ease, box-shadow 0.2s ease;
:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* Botones */
transition: background-color 0.15s ease;
:hover { background-color: var(--primary-hover); }

/* Input focus */
transition: border-color 0.2s ease, box-shadow 0.2s ease;
:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}
```

---

## 10. Estados de la UI

### Empty State (Sin resultados)
```
┌────────────────────────────┐
│                            │
│         🔍                 │
│                            │
│  No encontramos resultados │
│  para "asdfgh"             │
│                            │
│  Intenta con otra búsqueda │
│                            │
└────────────────────────────┘
```

### Loading State
```
┌────────────────────────────┐
│    [Skeleton Card 1]       │
│    [Skeleton Card 2]       │
│    [Skeleton Card 3]       │
└────────────────────────────┘
```

### Error State
```
┌────────────────────────────┐
│         ⚠️                  │
│  Error al cargar productos │
│  [Intentar de nuevo]       │
└────────────────────────────┘
```

---

## Resumen de Especificaciones

### Colores
- Primario: #2563eb (Azul)
- Fondo: #f9fafb (Gris claro)
- Cards: #ffffff (Blanco)
- Texto: #111827 (Gris oscuro)

### Tipografía
- Fuente: Inter
- Tamaños: 12px - 24px
- Pesos: 400 (normal), 600 (semibold), 700 (bold)

### Espaciado
- Cards padding: 16px
- Grid gap: 24px (desktop), 16px (mobile)
- Márgenes sección: 32px

### Grid
- Desktop: 4 columnas
- Tablet: 2 columnas
- Mobile: 1 columna

### Componentes
- Header sticky: 64px
- Input búsqueda: 56px
- Card producto: Auto height
- Botón: 40px

---

**Fecha:** 7 de diciembre de 2024
**Versión:** 1.0
