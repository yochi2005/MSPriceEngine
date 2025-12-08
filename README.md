# MSPriceEngine

**Price Search Engine for Mexico** - Compare prices across major online stores in Mexico using official APIs and data feeds.

A modern open-source project to help Mexican consumers find the best prices by integrating with official store APIs, XML/CSV/JSON feeds, and comparing products from Mercado Libre, Amazon MX, Walmart MX, Liverpool, Coppel, Sears, and more.

## Quick Links

- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Frontend:** http://localhost:5174 (React + Vite)
- **Complete Docs:** [docs/](docs/)
- **Integration Guide:** [docs/INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md)
- **API Credentials:** [docs/API_CREDENTIALS.md](docs/API_CREDENTIALS.md)
- **How to Add Products:** [docs/HOW_TO_ADD_PRODUCTS.md](docs/HOW_TO_ADD_PRODUCTS.md)

## Features

- REST API with advanced search and filtering
- **6 Store Integrations** (Mercado Libre, Amazon MX, Walmart MX, Liverpool, Coppel, Sears)
- Official API integration (no web scraping)
- XML/CSV/JSON feed parsers
- Advanced filters (price, store, category)
- Real-time product search
- SQLite/PostgreSQL support
- Docker deployment ready
- Modern React frontend with TailwindCSS
- Comprehensive documentation

## Tech Stack

### Backend
- **Framework**: Python 3.13 with FastAPI
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Integrations**: Official APIs + Feed Parsers (XML, CSV, JSON)
- **HTTP Client**: httpx (async)
- **Deployment**: Docker + Docker Compose

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS
- **Icons**: Lucide React
- **State Management**: React Hooks
- **Build Tool**: Vite

## Documentation

All documentation is available in the [docs/](docs/) directory:

- [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Installation and configuration
- [INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md) - How to use store integrations
- [API_CREDENTIALS.md](docs/API_CREDENTIALS.md) - How to obtain API credentials
- [HOW_TO_ADD_PRODUCTS.md](docs/HOW_TO_ADD_PRODUCTS.md) - Guide to add products manually
- [API_GUIDE.md](docs/API_GUIDE.md) - How to use the API
- [API_ENDPOINTS.md](docs/API_ENDPOINTS.md) - Endpoint reference

## Installation

### Backend Setup

```bash
# Clone repository
git clone git@github.com:yochi2005/MSPriceEngine.git
cd MSPriceEngine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python populate_db.py

# Run the API
uvicorn app.main:app --reload

# Access API at http://localhost:8000
```

### Frontend Setup

```bash
# Clone frontend repository
git clone git@github.com:yochi2005/MSPriceEngineFrontend.git
cd mspriceengine-frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Access frontend at http://localhost:5173
```

### Docker (Coming Soon)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the API
open http://localhost:8000/docs
```

## Store Integrations

### Currently Supported

| Store | Method | Status | Credentials Required |
|-------|--------|--------|---------------------|
| **Mercado Libre** | Public API | ✅ Active | None |
| **Amazon MX** | PA-API 5.0 | ⚠️ Pending | Access Key, Secret Key, Partner Tag |
| **Walmart MX** | Feed/API | ⚠️ Pending | Contact Walmart |
| **Liverpool** | Feed/API | ⚠️ Pending | Contact Liverpool |
| **Coppel** | JSON Feed | ⚠️ Pending | Feed URL |
| **Sears** | XML Feed | ⚠️ Pending | Feed URL |

See [API_CREDENTIALS.md](docs/API_CREDENTIALS.md) for detailed setup instructions.

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Calls

**Search products with filters:**
```bash
curl "http://localhost:8000/search?q=laptop&min_price=10000&max_price=30000&store_id=1"
```

**Search by category:**
```bash
curl "http://localhost:8000/search?q=iphone&category_id=2"
```

**Get product details:**
```bash
curl "http://localhost:8000/products/1"
```

**List stores:**
```bash
curl "http://localhost:8000/stores"
```

**List categories:**
```bash
curl "http://localhost:8000/categories"
```

## Importing Products

### Using Import Script

```bash
# Import from Mercado Libre with default queries
python import_products.py --all

# Import with custom queries
python import_products.py --queries "laptop,iphone,tablet"

# Import with custom limit per query
python import_products.py --all --limit 100
```

### Testing Integrations

```bash
# Test all integrations
python test_integrations.py

# Test specific store
python test_integrations.py --store mercadolibre
```

## Project Structure

```
MSPriceEngine/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   └── integrations/
│       ├── __init__.py
│       ├── base.py          # Base integration class
│       ├── api_adapter.py   # REST API adapter
│       ├── parsers/
│       │   ├── xml_parser.py
│       │   ├── csv_parser.py
│       │   └── json_parser.py
│       └── stores/
│           ├── mercadolibre.py
│           ├── amazon.py
│           ├── walmart.py
│           ├── liverpool.py
│           ├── coppel.py
│           └── sears.py
├── docs/                    # Documentation
├── tests/                   # Tests
├── import_products.py       # Product import script
├── test_integrations.py     # Integration tests
├── populate_db.py           # Sample data populator
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=sqlite:///./mspriceengine.db

# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/priceengine

# Store API Credentials
AMAZON_ACCESS_KEY=your_key
AMAZON_SECRET_KEY=your_secret
AMAZON_PARTNER_TAG=your_tag

COPPEL_FEED_URL=https://...
SEARS_FEED_URL=https://...
LIVERPOOL_FEED_URL=https://...
```

## Frontend Features

- **Search Interface**: Intuitive search with autocomplete
- **Advanced Filters**: Price range, store, category filters
- **Store Status**: Visual indicators of active integrations
- **Product Cards**: Color-coded badges by store
- **Responsive Design**: Mobile-first approach
- **Real-time Updates**: Instant filter application

## Testing

```bash
# Install dev dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Run specific test
pytest tests/test_integrations.py
```

## Current Status

### Implemented ✅
- FastAPI REST API with filters
- 6 store integrations (architecture complete)
- Mercado Libre integration (fully functional)
- XML/CSV/JSON feed parsers
- Product import system
- Advanced search filters (price, store, category)
- Modern React frontend
- SQLite database with migrations
- Docker-ready architecture
- Comprehensive documentation

### In Progress ⚠️
- Amazon MX integration (requires PA-API credentials)
- Walmart/Liverpool integrations (pending feed access)
- Coppel/Sears integrations (pending feed URLs)

### TODO 📋
- PostgreSQL production setup
- Price history tracking
- Product matching algorithm
- Automated price updates
- Email notifications
- Complete test suite
- CI/CD pipeline
- Production deployment

## Legal Disclaimer

This project uses **official APIs and authorized data feeds** instead of web scraping. However:

- Always respect store Terms of Service
- Use reasonable rate limiting
- Don't overload API servers
- Obtain proper API credentials
- Consult store partners for feed access
- Review legal requirements before production use

**No web scraping is performed** - all data comes from official sources.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - See LICENSE file for details

## Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/yochi2005/MSPriceEngine/issues)
- **Documentation**: See [docs/](docs/) directory
- **Email**: Contact for commercial inquiries

## Acknowledgments

- Built with FastAPI, React, and TailwindCSS
- Store integrations based on official APIs
- Community contributions welcome

---

**Note**: This project is actively maintained and under development. Star the repo to stay updated!
