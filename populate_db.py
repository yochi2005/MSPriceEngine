"""
Script to populate the database with stores, categories, and products.
Run with: python populate_db.py
"""
from app.database import SessionLocal, engine, Base
from app import models
from datetime import datetime

def populate_database():
    # Drop all existing tables and recreate with new schema
    print("Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)

    print("Creating database tables with new schema...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        # Create Stores
        print("\nCreating stores...")
        stores = [
            models.Store(name="Amazon MX", url="https://www.amazon.com.mx"),
            models.Store(name="Walmart MX", url="https://www.walmart.com.mx"),
            models.Store(name="Liverpool", url="https://www.liverpool.com.mx"),
            models.Store(name="Mercado Libre", url="https://www.mercadolibre.com.mx"),
            models.Store(name="Coppel", url="https://www.coppel.com"),
            models.Store(name="Elektra", url="https://www.elektra.com.mx"),
        ]

        for store in stores:
            db.add(store)
        db.commit()
        print(f"Created {len(stores)} stores")

        # Refresh to get IDs
        for store in stores:
            db.refresh(store)

        # Create Categories
        print("\nCreating categories...")
        categories = [
            models.Category(name="Laptops", slug="laptops", description="Laptops y computadoras portátiles"),
            models.Category(name="Smartphones", slug="smartphones", description="Teléfonos inteligentes"),
            models.Category(name="Tablets", slug="tablets", description="Tabletas electrónicas"),
            models.Category(name="Audio", slug="audio", description="Audífonos, bocinas y audio"),
            models.Category(name="TV y Video", slug="tv-video", description="Televisores y dispositivos de video"),
            models.Category(name="Gaming", slug="gaming", description="Consolas y videojuegos"),
            models.Category(name="Smartwatches", slug="smartwatches", description="Relojes inteligentes"),
            models.Category(name="Cámaras", slug="camaras", description="Cámaras fotográficas y accesorios"),
        ]

        for category in categories:
            db.add(category)
        db.commit()
        print(f"Created {len(categories)} categories")

        # Refresh to get IDs
        for category in categories:
            db.refresh(category)

        # Create category and store dictionaries for easier access
        store_dict = {store.name: store for store in stores}
        cat_dict = {cat.slug: cat for cat in categories}

        # Create Products
        print("\nCreating products...")
        products_data = [
            # Laptops
            {"name": "MacBook Air M2 13 pulgadas", "category": "laptops", "store": "Amazon MX", "price": 24999.00, "url": "https://amazon.com.mx/macbook-air-m2", "image": "https://m.media-amazon.com/images/I/71jG+e7roXL._AC_SL1500_.jpg"},
            {"name": "MacBook Air M2 13 pulgadas", "category": "laptops", "store": "Liverpool", "price": 25499.00, "url": "https://liverpool.com.mx/macbook-air", "image": "https://m.media-amazon.com/images/I/71jG+e7roXL._AC_SL1500_.jpg"},
            {"name": "Dell XPS 15", "category": "laptops", "store": "Amazon MX", "price": 32999.00, "url": "https://amazon.com.mx/dell-xps-15", "image": "https://m.media-amazon.com/images/I/71EJB9rGfqL._AC_SL1500_.jpg"},
            {"name": "Dell XPS 15", "category": "laptops", "store": "Coppel", "price": 33499.00, "url": "https://coppel.com/dell-xps-15", "image": "https://m.media-amazon.com/images/I/71EJB9rGfqL._AC_SL1500_.jpg"},
            {"name": "HP Pavilion 15", "category": "laptops", "store": "Walmart MX", "price": 12999.00, "url": "https://walmart.com.mx/hp-pavilion", "image": "https://m.media-amazon.com/images/I/71SLCWGaZFL._AC_SL1500_.jpg"},
            {"name": "HP Pavilion 15", "category": "laptops", "store": "Elektra", "price": 13499.00, "url": "https://elektra.com.mx/hp-pavilion", "image": "https://m.media-amazon.com/images/I/71SLCWGaZFL._AC_SL1500_.jpg"},
            {"name": "Lenovo ThinkPad X1 Carbon", "category": "laptops", "store": "Amazon MX", "price": 28999.00, "url": "https://amazon.com.mx/lenovo-thinkpad", "image": "https://m.media-amazon.com/images/I/61XKLHQGcwL._AC_SL1356_.jpg"},
            {"name": "ASUS ROG Zephyrus G14", "category": "laptops", "store": "Liverpool", "price": 35999.00, "url": "https://liverpool.com.mx/asus-rog", "image": "https://m.media-amazon.com/images/I/81bc8mA3nKL._AC_SL1500_.jpg"},
            {"name": "Acer Aspire 5", "category": "laptops", "store": "Mercado Libre", "price": 9999.00, "url": "https://mercadolibre.com.mx/acer-aspire-5", "image": "https://m.media-amazon.com/images/I/71uFWzaCVBL._AC_SL1500_.jpg"},

            # Smartphones
            {"name": "iPhone 15 Pro Max 256GB", "category": "smartphones", "store": "Amazon MX", "price": 29999.00, "url": "https://amazon.com.mx/iphone-15-pro-max", "image": "https://m.media-amazon.com/images/I/81SigpJN1KL._AC_SL1500_.jpg"},
            {"name": "iPhone 15 Pro Max 256GB", "category": "smartphones", "store": "Liverpool", "price": 30499.00, "url": "https://liverpool.com.mx/iphone-15", "image": "https://m.media-amazon.com/images/I/81SigpJN1KL._AC_SL1500_.jpg"},
            {"name": "iPhone 15 Pro Max 256GB", "category": "smartphones", "store": "Coppel", "price": 30999.00, "url": "https://coppel.com/iphone-15", "image": "https://m.media-amazon.com/images/I/81SigpJN1KL._AC_SL1500_.jpg"},
            {"name": "Samsung Galaxy S24 Ultra", "category": "smartphones", "store": "Amazon MX", "price": 25999.00, "url": "https://amazon.com.mx/samsung-s24-ultra", "image": "https://m.media-amazon.com/images/I/71WRwQHsJvL._AC_SL1500_.jpg"},
            {"name": "Samsung Galaxy S24 Ultra", "category": "smartphones", "store": "Walmart MX", "price": 26499.00, "url": "https://walmart.com.mx/samsung-s24", "image": "https://m.media-amazon.com/images/I/71WRwQHsJvL._AC_SL1500_.jpg"},
            {"name": "Samsung Galaxy S24 Ultra", "category": "smartphones", "store": "Elektra", "price": 26999.00, "url": "https://elektra.com.mx/samsung-s24", "image": "https://m.media-amazon.com/images/I/71WRwQHsJvL._AC_SL1500_.jpg"},
            {"name": "Xiaomi 13 Pro", "category": "smartphones", "store": "Mercado Libre", "price": 14999.00, "url": "https://mercadolibre.com.mx/xiaomi-13-pro", "image": "https://m.media-amazon.com/images/I/61i2n4iFCFL._AC_SL1000_.jpg"},
            {"name": "Google Pixel 8 Pro", "category": "smartphones", "store": "Amazon MX", "price": 18999.00, "url": "https://amazon.com.mx/pixel-8-pro", "image": "https://m.media-amazon.com/images/I/71IYc6q0gGL._AC_SL1500_.jpg"},
            {"name": "OnePlus 12", "category": "smartphones", "store": "Mercado Libre", "price": 16999.00, "url": "https://mercadolibre.com.mx/oneplus-12", "image": "https://m.media-amazon.com/images/I/61BfF5pjP3L._AC_SL1500_.jpg"},

            # Tablets
            {"name": "iPad Pro 12.9 M2 128GB", "category": "tablets", "store": "Amazon MX", "price": 22999.00, "url": "https://amazon.com.mx/ipad-pro-m2", "image": "https://m.media-amazon.com/images/I/81a2ADMF3ML._AC_SL1500_.jpg"},
            {"name": "iPad Pro 12.9 M2 128GB", "category": "tablets", "store": "Liverpool", "price": 23499.00, "url": "https://liverpool.com.mx/ipad-pro", "image": "https://m.media-amazon.com/images/I/81a2ADMF3ML._AC_SL1500_.jpg"},
            {"name": "Samsung Galaxy Tab S9", "category": "tablets", "store": "Walmart MX", "price": 14999.00, "url": "https://walmart.com.mx/galaxy-tab-s9", "image": "https://m.media-amazon.com/images/I/61AaqVXfx4L._AC_SL1500_.jpg"},
            {"name": "Samsung Galaxy Tab S9", "category": "tablets", "store": "Elektra", "price": 15499.00, "url": "https://elektra.com.mx/galaxy-tab", "image": "https://m.media-amazon.com/images/I/61AaqVXfx4L._AC_SL1500_.jpg"},
            {"name": "iPad Air M1 64GB", "category": "tablets", "store": "Coppel", "price": 12999.00, "url": "https://coppel.com/ipad-air", "image": "https://m.media-amazon.com/images/I/61ngBWZJiGL._AC_SL1500_.jpg"},

            # Audio
            {"name": "AirPods Pro 2da Gen", "category": "audio", "store": "Amazon MX", "price": 5999.00, "url": "https://amazon.com.mx/airpods-pro", "image": "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg"},
            {"name": "AirPods Pro 2da Gen", "category": "audio", "store": "Liverpool", "price": 6199.00, "url": "https://liverpool.com.mx/airpods", "image": "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg"},
            {"name": "Sony WH-1000XM5", "category": "audio", "store": "Amazon MX", "price": 7999.00, "url": "https://amazon.com.mx/sony-wh1000xm5", "image": "https://m.media-amazon.com/images/I/61vKS+MJZ7L._AC_SL1500_.jpg"},
            {"name": "Sony WH-1000XM5", "category": "audio", "store": "Walmart MX", "price": 8299.00, "url": "https://walmart.com.mx/sony-headphones", "image": "https://m.media-amazon.com/images/I/61vKS+MJZ7L._AC_SL1500_.jpg"},
            {"name": "Bose QuietComfort 45", "category": "audio", "store": "Liverpool", "price": 6999.00, "url": "https://liverpool.com.mx/bose-qc45", "image": "https://m.media-amazon.com/images/I/51AagGGUypL._AC_SL1000_.jpg"},
            {"name": "JBL Flip 6", "category": "audio", "store": "Mercado Libre", "price": 2499.00, "url": "https://mercadolibre.com.mx/jbl-flip-6", "image": "https://m.media-amazon.com/images/I/81HgYBGWomL._AC_SL1500_.jpg"},
            {"name": "Beats Studio Pro", "category": "audio", "store": "Coppel", "price": 5999.00, "url": "https://coppel.com/beats-studio", "image": "https://m.media-amazon.com/images/I/51vVRXXI2cL._AC_SL1500_.jpg"},

            # TV y Video
            {"name": "Samsung QLED 55 4K", "category": "tv-video", "store": "Liverpool", "price": 18999.00, "url": "https://liverpool.com.mx/samsung-qled", "image": "https://m.media-amazon.com/images/I/81rfT4h1ueL._AC_SL1500_.jpg"},
            {"name": "Samsung QLED 55 4K", "category": "tv-video", "store": "Coppel", "price": 19499.00, "url": "https://coppel.com/samsung-tv", "image": "https://m.media-amazon.com/images/I/81rfT4h1ueL._AC_SL1500_.jpg"},
            {"name": "LG OLED 55 4K", "category": "tv-video", "store": "Amazon MX", "price": 24999.00, "url": "https://amazon.com.mx/lg-oled", "image": "https://m.media-amazon.com/images/I/81S8h-+VWWL._AC_SL1500_.jpg"},
            {"name": "LG OLED 55 4K", "category": "tv-video", "store": "Elektra", "price": 25499.00, "url": "https://elektra.com.mx/lg-oled", "image": "https://m.media-amazon.com/images/I/81S8h-+VWWL._AC_SL1500_.jpg"},
            {"name": "Sony Bravia 65 4K", "category": "tv-video", "store": "Walmart MX", "price": 21999.00, "url": "https://walmart.com.mx/sony-bravia", "image": "https://m.media-amazon.com/images/I/81Q2oKTCqyL._AC_SL1500_.jpg"},

            # Gaming
            {"name": "PlayStation 5", "category": "gaming", "store": "Amazon MX", "price": 13999.00, "url": "https://amazon.com.mx/ps5", "image": "https://m.media-amazon.com/images/I/51DKubiQEyL._AC_SL1001_.jpg"},
            {"name": "PlayStation 5", "category": "gaming", "store": "Liverpool", "price": 14299.00, "url": "https://liverpool.com.mx/ps5", "image": "https://m.media-amazon.com/images/I/51DKubiQEyL._AC_SL1001_.jpg"},
            {"name": "PlayStation 5", "category": "gaming", "store": "Elektra", "price": 14499.00, "url": "https://elektra.com.mx/ps5", "image": "https://m.media-amazon.com/images/I/51DKubiQEyL._AC_SL1001_.jpg"},
            {"name": "Xbox Series X", "category": "gaming", "store": "Walmart MX", "price": 12999.00, "url": "https://walmart.com.mx/xbox-series-x", "image": "https://m.media-amazon.com/images/I/51lbX8GtnJL._AC_SL1000_.jpg"},
            {"name": "Xbox Series X", "category": "gaming", "store": "Coppel", "price": 13299.00, "url": "https://coppel.com/xbox", "image": "https://m.media-amazon.com/images/I/51lbX8GtnJL._AC_SL1000_.jpg"},
            {"name": "Nintendo Switch OLED", "category": "gaming", "store": "Amazon MX", "price": 7999.00, "url": "https://amazon.com.mx/switch-oled", "image": "https://m.media-amazon.com/images/I/61xZJwgVyIL._AC_SL1500_.jpg"},
            {"name": "Nintendo Switch OLED", "category": "gaming", "store": "Mercado Libre", "price": 8299.00, "url": "https://mercadolibre.com.mx/switch-oled", "image": "https://m.media-amazon.com/images/I/61xZJwgVyIL._AC_SL1500_.jpg"},

            # Smartwatches
            {"name": "Apple Watch Series 9 45mm", "category": "smartwatches", "store": "Amazon MX", "price": 9999.00, "url": "https://amazon.com.mx/apple-watch-9", "image": "https://m.media-amazon.com/images/I/71rAcY6b+hL._AC_SL1500_.jpg"},
            {"name": "Apple Watch Series 9 45mm", "category": "smartwatches", "store": "Liverpool", "price": 10299.00, "url": "https://liverpool.com.mx/apple-watch", "image": "https://m.media-amazon.com/images/I/71rAcY6b+hL._AC_SL1500_.jpg"},
            {"name": "Samsung Galaxy Watch 6", "category": "smartwatches", "store": "Walmart MX", "price": 6999.00, "url": "https://walmart.com.mx/galaxy-watch-6", "image": "https://m.media-amazon.com/images/I/61Z7vlBZr+L._AC_SL1500_.jpg"},
            {"name": "Samsung Galaxy Watch 6", "category": "smartwatches", "store": "Elektra", "price": 7299.00, "url": "https://elektra.com.mx/galaxy-watch", "image": "https://m.media-amazon.com/images/I/61Z7vlBZr+L._AC_SL1500_.jpg"},
            {"name": "Garmin Fenix 7", "category": "smartwatches", "store": "Amazon MX", "price": 12999.00, "url": "https://amazon.com.mx/garmin-fenix-7", "image": "https://m.media-amazon.com/images/I/61ufmSCVb+L._AC_SL1500_.jpg"},

            # Cámaras
            {"name": "Canon EOS R6 Mark II", "category": "camaras", "store": "Amazon MX", "price": 45999.00, "url": "https://amazon.com.mx/canon-r6-mark2", "image": "https://m.media-amazon.com/images/I/81Jrt03aKNL._AC_SL1500_.jpg"},
            {"name": "Canon EOS R6 Mark II", "category": "camaras", "store": "Liverpool", "price": 46999.00, "url": "https://liverpool.com.mx/canon-r6", "image": "https://m.media-amazon.com/images/I/81Jrt03aKNL._AC_SL1500_.jpg"},
            {"name": "Sony A7 IV", "category": "camaras", "store": "Amazon MX", "price": 52999.00, "url": "https://amazon.com.mx/sony-a7-iv", "image": "https://m.media-amazon.com/images/I/71rC8x5BrsL._AC_SL1500_.jpg"},
            {"name": "GoPro HERO 12", "category": "camaras", "store": "Walmart MX", "price": 8999.00, "url": "https://walmart.com.mx/gopro-hero-12", "image": "https://m.media-amazon.com/images/I/61EZe+w1GqL._AC_SL1500_.jpg"},
            {"name": "GoPro HERO 12", "category": "camaras", "store": "Mercado Libre", "price": 9299.00, "url": "https://mercadolibre.com.mx/gopro-12", "image": "https://m.media-amazon.com/images/I/61EZe+w1GqL._AC_SL1500_.jpg"},
        ]

        products_created = []
        for p_data in products_data:
            product = models.Product(
                name=p_data["name"],
                store_id=store_dict[p_data["store"]].id,
                category_id=cat_dict[p_data["category"]].id,
                store_url=p_data["url"],
                price=p_data["price"],
                image_url=p_data["image"],
                currency="MXN",
                available=1
            )
            products_created.append(product)
            db.add(product)

        db.commit()
        print(f"Created {len(products_created)} products")

        # Summary
        print("\n" + "="*50)
        print("DATABASE POPULATED SUCCESSFULLY!")
        print("="*50)
        print(f"Stores: {len(stores)}")
        print(f"Categories: {len(categories)}")
        print(f"Products: {len(products_created)}")
        print("="*50)

    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_database()
