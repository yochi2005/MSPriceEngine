"""FastAPI application - Main entry point."""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import logging

from . import models, schemas
from .database import get_db, init_db, engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MSPriceEngine API",
    description="Price Search Engine for Mexico - Compare prices across major online stores",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API information."""
    return {
        "name": "MSPriceEngine API",
        "version": "0.1.0",
        "description": "Price Search Engine for Mexico",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/search", response_model=schemas.ProductSearchResponse, tags=["Products"])
def search_products(
    q: str = Query(..., min_length=2, description="Search query"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    limit: int = Query(50, le=100, description="Number of results"),
    offset: int = Query(0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    Search products by name.

    - **q**: Search query (minimum 2 characters)
    - **store_id**: Optional filter by store
    - **min_price**: Optional minimum price filter
    - **max_price**: Optional maximum price filter
    - **limit**: Maximum results to return (default 50, max 100)
    - **offset**: Offset for pagination (default 0)
    """
    # Build query
    query = db.query(models.Product).filter(models.Product.name.ilike(f"%{q}%"))

    # Apply filters
    if store_id:
        query = query.filter(models.Product.store_id == store_id)
    if min_price:
        query = query.filter(models.Product.price >= min_price)
    if max_price:
        query = query.filter(models.Product.price <= max_price)

    # Get total count
    total = query.count()

    # Get paginated results
    products = query.order_by(models.Product.price).offset(offset).limit(limit).all()

    return schemas.ProductSearchResponse(total=total, products=products)


@app.get("/products/{product_id}", response_model=schemas.Product, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get product by ID.

    - **product_id**: Product ID
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/stores", response_model=list[schemas.Store], tags=["Stores"])
def get_stores(db: Session = Depends(get_db)):
    """Get all available stores."""
    stores = db.query(models.Store).all()
    return stores


@app.get("/stores/{store_id}", response_model=schemas.Store, tags=["Stores"])
def get_store(store_id: int, db: Session = Depends(get_db)):
    """
    Get store by ID.

    - **store_id**: Store ID
    """
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@app.get("/stores/{store_id}/products", response_model=list[schemas.Product], tags=["Stores"])
def get_store_products(
    store_id: int,
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """
    Get all products from a specific store.

    - **store_id**: Store ID
    - **limit**: Maximum results (default 50, max 100)
    - **offset**: Offset for pagination
    """
    # Verify store exists
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    products = db.query(models.Product)\
        .filter(models.Product.store_id == store_id)\
        .offset(offset)\
        .limit(limit)\
        .all()

    return products
