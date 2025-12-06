"""Scheduler for periodic scraping tasks."""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime

from .database import SessionLocal
from .scrapers import AmazonScraper, WalmartScraper, LiverpoolScraper
from . import models

logger = logging.getLogger(__name__)


class ScraperScheduler:
    """Manages scheduled scraping tasks."""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scrapers = {
            'amazon': AmazonScraper(),
            'walmart': WalmartScraper(),
            'liverpool': LiverpoolScraper()
        }

    async def scrape_store(self, store_name: str, queries: list[str]):
        """
        Scrape a store for given queries.

        Args:
            store_name: Name of the store ('amazon', 'walmart', 'liverpool')
            queries: List of search queries
        """
        logger.info(f"Starting scrape for {store_name}")
        db = SessionLocal()

        try:
            scraper = self.scrapers.get(store_name.lower())
            if not scraper:
                logger.error(f"Unknown store: {store_name}")
                return

            # Get or create store in database
            store = db.query(models.Store).filter(models.Store.name == scraper.store_name).first()
            if not store:
                store = models.Store(name=scraper.store_name, url=scraper.base_url)
                db.add(store)
                db.commit()
                db.refresh(store)

            # Scrape each query
            for query in queries:
                try:
                    products = await scraper.scrape_search(query, max_results=20)
                    logger.info(f"Found {len(products)} products for query '{query}' on {store_name}")

                    # Save products to database
                    for product_data in products:
                        # Check if product already exists (by SKU and store)
                        existing = db.query(models.Product).filter(
                            models.Product.sku == product_data.get('sku'),
                            models.Product.store_id == store.id
                        ).first()

                        if existing:
                            # Update existing product
                            existing.price = product_data['price']
                            existing.available = 1 if product_data.get('available', True) else 0
                            existing.last_updated = datetime.utcnow()
                        else:
                            # Create new product
                            new_product = models.Product(
                                name=product_data['name'],
                                store_id=store.id,
                                store_url=product_data['url'],
                                sku=product_data.get('sku'),
                                price=product_data['price'],
                                image_url=product_data.get('image_url'),
                                available=1 if product_data.get('available', True) else 0
                            )
                            db.add(new_product)

                    db.commit()
                    logger.info(f"Saved products for query '{query}'")

                except Exception as e:
                    logger.error(f"Error scraping query '{query}' on {store_name}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error in scrape_store for {store_name}: {e}")
        finally:
            db.close()

        logger.info(f"Finished scrape for {store_name}")

    def run_daily_scrape(self):
        """Run daily scraping for all stores."""
        import asyncio

        logger.info("Starting daily scrape job")

        # Define popular queries to scrape
        queries = [
            "laptop",
            "iphone",
            "samsung galaxy",
            "nintendo switch",
            "playstation 5",
            "xbox",
            "airpods",
            "tablet"
        ]

        # Run scraping tasks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Scrape Amazon (currently implemented)
            loop.run_until_complete(self.scrape_store('amazon', queries))

            # TODO: Enable when Walmart and Liverpool scrapers are implemented
            # loop.run_until_complete(self.scrape_store('walmart', queries))
            # loop.run_until_complete(self.scrape_store('liverpool', queries))

        finally:
            loop.close()

        logger.info("Daily scrape job completed")

    def start(self):
        """Start the scheduler."""
        # Run daily at 3:00 AM
        self.scheduler.add_job(
            self.run_daily_scrape,
            trigger=CronTrigger(hour=3, minute=0),
            id='daily_scrape',
            name='Daily product scraping',
            replace_existing=True
        )

        self.scheduler.start()
        logger.info("Scheduler started - daily scraping at 3:00 AM")

    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")

    def run_now(self):
        """Manually trigger scraping job now (for testing)."""
        logger.info("Manually triggering scrape job")
        self.run_daily_scrape()


# Global scheduler instance
scheduler = ScraperScheduler()
