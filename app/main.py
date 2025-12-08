"""FastAPI application - Main entry point."""
from fastapi import FastAPI, Depends, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
import logging
import math

from . import models, schemas
from .database import get_db, init_db, engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Magic Solutions Price API",
    description="Price Search Engine for Mexico - Compare prices across major online stores",
    version="0.2.0",
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
        "name": "Magic Solutions Price API",
        "version": "0.2.0",
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
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    per_page: int = Query(50, ge=1, le=100, description="Results per page (max 100)"),
    db: Session = Depends(get_db)
):
    """
    Search products by name with filters and pagination.

    - **q**: Search query (minimum 2 characters)
    - **store_id**: Optional filter by store
    - **category_id**: Optional filter by category
    - **min_price**: Optional minimum price filter
    - **max_price**: Optional maximum price filter
    - **page**: Page number (default 1)
    - **per_page**: Results per page (default 50, max 100)
    """
    # Build query
    query = db.query(models.Product).filter(models.Product.name.ilike(f"%{q}%"))

    # Apply filters
    if store_id:
        query = query.filter(models.Product.store_id == store_id)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if min_price:
        query = query.filter(models.Product.price >= min_price)
    if max_price:
        query = query.filter(models.Product.price <= max_price)

    # Get total count
    total = query.count()

    # Calculate pagination
    total_pages = math.ceil(total / per_page) if total > 0 else 0
    offset = (page - 1) * per_page

    # Get paginated results
    products = query.order_by(models.Product.price).offset(offset).limit(per_page).all()

    return schemas.ProductSearchResponse(
        products=products,
        pagination=schemas.PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages
        )
    )


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


@app.get("/categories", response_model=list[schemas.Category], tags=["Categories"])
def get_categories(db: Session = Depends(get_db)):
    """Get all available product categories."""
    categories = db.query(models.Category).order_by(models.Category.name).all()
    return categories


@app.get("/categories/{category_id}", response_model=schemas.Category, tags=["Categories"])
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get category by ID.

    - **category_id**: Category ID
    """
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.get("/categories/{category_id}/products", response_model=schemas.ProductSearchResponse, tags=["Categories"])
def get_category_products(
    category_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all products from a specific category.

    - **category_id**: Category ID
    - **page**: Page number (default 1)
    - **per_page**: Results per page (default 50, max 100)
    """
    # Verify category exists
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Build query
    query = db.query(models.Product).filter(models.Product.category_id == category_id)

    # Get total count
    total = query.count()

    # Calculate pagination
    total_pages = math.ceil(total / per_page) if total > 0 else 0
    offset = (page - 1) * per_page

    # Get paginated results
    products = query.order_by(models.Product.price).offset(offset).limit(per_page).all()

    return schemas.ProductSearchResponse(
        products=products,
        pagination=schemas.PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages
        )
    )


@app.post("/products/bulk", response_model=schemas.BulkCreateResponse, tags=["Products"])
def bulk_create_products(
    bulk_data: schemas.ProductBulkCreate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Bulk create products.

    - **products**: List of products to create
    """
    created = 0
    failed = 0
    errors = []

    for idx, product_data in enumerate(bulk_data.products):
        try:
            # Verify store exists
            store = db.query(models.Store).filter(models.Store.id == product_data.store_id).first()
            if not store:
                errors.append(f"Product {idx}: Store ID {product_data.store_id} not found")
                failed += 1
                continue

            # Verify category exists if provided
            if product_data.category_id:
                category = db.query(models.Category).filter(models.Category.id == product_data.category_id).first()
                if not category:
                    errors.append(f"Product {idx}: Category ID {product_data.category_id} not found")
                    failed += 1
                    continue

            # Create product
            db_product = models.Product(**product_data.model_dump())
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            created += 1

        except IntegrityError as e:
            db.rollback()
            errors.append(f"Product {idx}: Integrity error - {str(e.orig)}")
            failed += 1
        except Exception as e:
            db.rollback()
            errors.append(f"Product {idx}: {str(e)}")
            failed += 1

    return schemas.BulkCreateResponse(
        created=created,
        failed=failed,
        errors=errors
    )
