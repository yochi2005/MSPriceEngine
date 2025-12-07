# Documentación de MSPriceEngine

Bienvenido a la documentación completa de MSPriceEngine - Price Search Engine para México.

## Índice de Documentación

### 📚 Para Nuevos Usuarios

1. **[README Principal](../README.md)**
   - Descripción general del proyecto
   - Quick start
   - Features principales

2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** ⭐ COMIENZA AQUÍ
   - Instalación paso a paso
   - Configuración del ambiente virtual
   - Rutas importantes del proyecto
   - Dependencias explicadas
   - Troubleshooting

### 🔧 Para Desarrolladores

3. **[ARCHITECTURE.md](ARCHITECTURE.md)**
   - Explicación técnica completa
   - Conceptos importantes (FastAPI, Pydantic, SQLAlchemy)
   - Arquitectura general con diagramas
   - Código explicado línea por línea
   - Cómo funciona el scraping
   - Próximas mejoras recomendadas

4. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**
   - Estructura de directorios
   - Descripción de cada archivo
   - Flujo de datos
   - Patrones de diseño
   - Convenciones de código

### 🌐 Para Usuarios de la API

5. **[API_GUIDE.md](API_GUIDE.md)** ⭐ GUÍA PRINCIPAL
   - Cómo usar la API
   - Ejemplos con Python, JavaScript, cURL
   - Paginación
   - Manejo de errores
   - Buenas prácticas

6. **[API_ENDPOINTS.md](API_ENDPOINTS.md)**
   - Referencia rápida de todos los endpoints
   - Parámetros detallados
   - Esquemas de response
   - Códigos de estado HTTP

### 💻 Para Frontend Developers

7. **[FRONTEND_REQUIREMENTS.md](FRONTEND_REQUIREMENTS.md)**
   - Requerimientos funcionales y no funcionales
   - Stack tecnológico recomendado (React + Vite)
   - Wireframes y diseño UI/UX
   - Integración con API backend
   - Guía de desarrollo paso a paso

### 📄 Documentos Adicionales

8. **[RESUMEN_COMPLETO.md](../RESUMEN_COMPLETO.md)**
   - Resumen ejecutivo del proyecto
   - Estado actual vs. pendiente
   - Comparación API vs. Página Web
   - Próximos pasos

9. **[MSPriceEngine_Explanation.txt](../MSPriceEngine_Explanation.txt)**
   - Explicación técnica en formato texto plano
   - Mismo contenido que ARCHITECTURE.md

---

## Guía Rápida de Inicio

### 1. Instalación

```bash
# Clonar repositorio
git clone git@github.com:yochi2005/MSPriceEngine.git
cd MSPriceEngine

# Crear ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar

```bash
# Iniciar servidor
uvicorn app.main:app --reload

# Abrir documentación interactiva
http://localhost:8000/docs
```

### 3. Probar

```bash
# Health check
curl http://localhost:8000/health

# Buscar productos (inicialmente vacío)
curl http://localhost:8000/search?q=laptop
```

---

## Documentación por Audiencia

### Si eres...

**👨‍💻 Nuevo en el Proyecto:**
1. Leer [README.md](../README.md)
2. Seguir [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. Explorar [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

**🔨 Backend Developer:**
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Entender la arquitectura
2. [SETUP_GUIDE.md](SETUP_GUIDE.md) - Setup local
3. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Estructura de código

**🎨 Frontend Developer:**
1. [FRONTEND_REQUIREMENTS.md](FRONTEND_REQUIREMENTS.md) - Specs completas
2. [API_GUIDE.md](API_GUIDE.md) - Cómo consumir la API
3. [API_ENDPOINTS.md](API_ENDPOINTS.md) - Referencia de endpoints

**🧪 QA/Tester:**
1. [API_ENDPOINTS.md](API_ENDPOINTS.md) - Endpoints a probar
2. [API_GUIDE.md](API_GUIDE.md) - Casos de uso
3. `tests/test_api.py` - Tests automatizados

**📊 Product Manager:**
1. [RESUMEN_COMPLETO.md](../RESUMEN_COMPLETO.md) - Overview
2. [FRONTEND_REQUIREMENTS.md](FRONTEND_REQUIREMENTS.md) - Features
3. [README.md](../README.md) - Descripción general

---

## Estructura de la Documentación

```
docs/
├── README.md                    ← Este archivo (índice)
├── SETUP_GUIDE.md              ← Instalación y configuración
├── ARCHITECTURE.md             ← Arquitectura técnica completa
├── PROJECT_STRUCTURE.md        ← Estructura de directorios y archivos
├── API_GUIDE.md                ← Guía de uso de la API
├── API_ENDPOINTS.md            ← Referencia rápida de endpoints
└── FRONTEND_REQUIREMENTS.md    ← Especificaciones del frontend
```

---

## Temas Cubiertos

### Conceptos Técnicos

- ✅ FastAPI y async/await
- ✅ Pydantic para validación
- ✅ SQLAlchemy ORM
- ✅ Web scraping con BeautifulSoup
- ✅ Dependency Injection
- ✅ RESTful API design
- ✅ Docker containerization

### Guías Prácticas

- ✅ Instalación paso a paso
- ✅ Configuración de ambiente virtual
- ✅ Uso de la API con ejemplos
- ✅ Cómo agregar nuevos scrapers
- ✅ Deploy con Docker
- ✅ Testing

### Especificaciones

- ✅ Todos los endpoints documentados
- ✅ Esquemas de request/response
- ✅ Códigos de error
- ✅ Requerimientos del frontend
- ✅ Stack tecnológico recomendado

---

## Convenciones en la Documentación

### Símbolos

- ⭐ - Documento importante/recomendado
- ✅ - Completado/Implementado
- ❌ - No implementado
- ⚠️ - Advertencia/Cuidado
- 📚 - Referencia
- 🔧 - Técnico
- 💡 - Tip/Consejo

### Bloques de Código

```bash
# Comandos de terminal
```

```python
# Código Python
```

```json
# Respuestas JSON
```

### Niveles de Encabezado

- `#` - Título del documento
- `##` - Sección principal
- `###` - Subsección
- `####` - Detalle

---

## Documentación Interactiva

Además de estos documentos, la API incluye documentación interactiva:

### Swagger UI
```
http://localhost:8000/docs
```

**Features:**
- Probar endpoints en vivo
- Ver esquemas de datos
- Generar requests de ejemplo
- Descargar OpenAPI spec

### ReDoc
```
http://localhost:8000/redoc
```

**Features:**
- Vista de solo lectura más limpia
- Mejor para leer que para probar
- Búsqueda integrada

---

## Actualizaciones

Esta documentación se actualiza con cada release del proyecto.

**Versión Actual:** 0.1.0
**Última Actualización:** 6 de diciembre de 2024

### Changelog de Documentación

**v0.1.0 (6 dic 2024)**
- Documentación inicial completa
- 7 documentos principales
- Guías de instalación, uso y arquitectura
- Especificaciones de frontend

---

## Contribuir a la Documentación

¿Encontraste un error o quieres mejorar la documentación?

1. Fork el repositorio
2. Edita los archivos en `docs/`
3. Envía un Pull Request
4. Sigue el [estilo de escritura](#convenciones-en-la-documentación)

### Guía de Estilo

- Usa lenguaje claro y simple
- Incluye ejemplos de código
- Agrega diagramas cuando sea posible
- Actualiza el índice si añades nuevos docs
- Usa markdown válido

---

## Recursos Externos

### Tecnologías Usadas

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Tutoriales Relacionados

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Web Scraping with Python](https://realpython.com/beautiful-soup-web-scraper-python/)

---

## Soporte

Si tienes preguntas sobre la documentación:

- **GitHub Issues:** https://github.com/yochi2005/MSPriceEngine/issues
- **Discusiones:** https://github.com/yochi2005/MSPriceEngine/discussions

---

## Licencia

Esta documentación está bajo la misma licencia MIT que el proyecto.

Ver [LICENSE](../LICENSE) para más detalles.

---

**¡Gracias por usar MSPriceEngine!** 🚀

Si esta documentación te fue útil, considera darle una estrella al proyecto en GitHub.
