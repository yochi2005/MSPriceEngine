# MSPriceEngine 🏷️

**Price Search Engine for Mexico** - Compare prices across major online stores in Mexico.

An open-source project to help Mexican consumers find the best prices by scraping and comparing products from Amazon MX, Walmart MX, Liverpool, and more.

## 🚀 Features

- ✅ REST API for product search
- ✅ Multiple store support (Amazon MX, Walmart MX, Liverpool)
- ✅ Automated daily price updates
- ✅ SQLite/PostgreSQL support
- ✅ Docker deployment ready
- ✅ Swagger UI documentation

## 📋 Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Scraping**: httpx + BeautifulSoup4
- **Scheduler**: APScheduler
- **Deployment**: Docker + Docker Compose

## 🛠️ Installation

### Option 1: Local Development

```bash
# Clone repository
git clone <repository-url>
cd MSPriceEngine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

### Option 2: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the API
open http://localhost:8000/docs
```

## 📖 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Calls

**Search products:**
```bash
curl "http://localhost:8000/search?q=iphone&min_price=5000&max_price=20000"
```

**Get product details:**
```bash
curl "http://localhost:8000/products/1"
```

**List stores:**
```bash
curl "http://localhost:8000/stores"
```

## 📁 Project Structure

```
MSPriceEngine/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   ├── scheduler.py         # Scraping scheduler
│   └── scrapers/
│       ├── __init__.py
│       ├── base.py          # Base scraper class
│       ├── amazon.py        # Amazon MX scraper
│       ├── walmart.py       # Walmart MX scraper
│       └── liverpool.py     # Liverpool scraper
├── tests/
│   └── __init__.py
├── data/                    # SQLite database (gitignored)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=sqlite:///./data/price_search.db

# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/priceengine

# Scheduler
ENABLE_SCHEDULER=false
SCRAPING_HOUR=3
```

## 🤖 Running Scrapers

The scheduler runs automatically at 3:00 AM daily. To manually trigger:

```python
from app.scheduler import scheduler
scheduler.run_now()
```

## 🧪 Testing

```bash
# Install dev dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 📊 Current Status

### Implemented ✅
- Amazon MX scraper (basic)
- FastAPI REST API
- SQLite database
- Docker deployment
- Swagger documentation

### TODO 🚧
- Complete Walmart MX scraper (needs JS rendering)
- Complete Liverpool scraper
- Add more stores (Mercado Libre, Coppel, etc.)
- Price history tracking
- Product matching algorithm
- Tests suite
- CI/CD pipeline

## ⚠️ Legal Disclaimer

This project is for **educational purposes only**. Web scraping may violate the Terms of Service of some websites. Always:
- Respect `robots.txt`
- Use reasonable rate limiting
- Don't overload servers
- Consult with a lawyer before production use

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🔗 Links

- **Documentation**: Coming soon
- **Issues**: Report bugs on GitHub
- **Discussions**: Join our community

---

Made with ❤️ for the Mexican tech community
