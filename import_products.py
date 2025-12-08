"""
Script para importar productos desde integraciones (Mercado Libre, etc.)

Uso:
    python import_products.py --store mercadolibre --queries "laptop,iphone,tablet"
    python import_products.py --all  # Importar todos los queries predefinidos
"""
import asyncio
import argparse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal, init_db
from app import models
from app.integrations.stores.mercadolibre import MercadoLibreIntegration
import re


def create_slug(text: str) -> str:
    """Crea un slug a partir de un texto."""
    # Convertir a minúsculas y remover caracteres especiales
    text = text.lower()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    # Reemplazar espacios y caracteres no alfanuméricos con guiones
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remover guiones al inicio y final
    text = text.strip('-')
    return text


# Queries predefinidos para importar productos populares
DEFAULT_QUERIES = [
    "laptop",
    "iphone",
    "samsung galaxy",
    "nintendo switch",
    "playstation 5",
    "xbox",
    "airpods",
    "tablet",
    "smart tv",
    "audifonos",
    "mouse gamer",
    "teclado mecanico"
]


async def import_from_mercadolibre(db: Session, queries: list[str], limit_per_query: int = 50):
    """
    Importa productos desde Mercado Libre.

    Args:
        db: Sesión de base de datos
        queries: Lista de términos de búsqueda
        limit_per_query: Productos por término de búsqueda
    """
    print("=" * 60)
    print("IMPORTANDO PRODUCTOS DE MERCADO LIBRE")
    print("=" * 60)

    # Inicializar integración
    ml = MercadoLibreIntegration()

    # Probar conexión primero
    print("\n1. Probando conexión con Mercado Libre...")
    connected = await ml.test_connection()
    if not connected:
        print("✗ No se pudo conectar a Mercado Libre")
        return

    print("✓ Conexión exitosa")

    # Obtener o crear tienda
    print("\n2. Configurando tienda en base de datos...")
    store = db.query(models.Store).filter(models.Store.name == "Mercado Libre").first()
    if not store:
        store = models.Store(
            name="Mercado Libre",
            url="https://www.mercadolibre.com.mx"
        )
        db.add(store)
        db.commit()
        db.refresh(store)
        print(f"✓ Tienda creada: {store.name} (ID: {store.id})")
    else:
        print(f"✓ Tienda encontrada: {store.name} (ID: {store.id})")

    # Obtener o crear categorías
    print("\n3. Configurando categorías...")
    categories = {}
    category_names = [
        "Electrónica",
        "Computación",
        "Celulares",
        "Videojuegos",
        "Audio",
        "Hogar"
    ]

    for cat_name in category_names:
        cat = db.query(models.Category).filter(models.Category.name == cat_name).first()
        if not cat:
            cat = models.Category(
                name=cat_name,
                slug=create_slug(cat_name),
                description=f"Productos de {cat_name}"
            )
            db.add(cat)
            db.commit()
            db.refresh(cat)
        categories[cat_name.lower()] = cat
        print(f"  ✓ {cat_name} (ID: {cat.id})")

    # Mapeo de queries a categorías
    query_to_category = {
        "laptop": categories.get("computación"),
        "iphone": categories.get("celulares"),
        "samsung galaxy": categories.get("celulares"),
        "nintendo switch": categories.get("videojuegos"),
        "playstation 5": categories.get("videojuegos"),
        "xbox": categories.get("videojuegos"),
        "airpods": categories.get("audio"),
        "audifonos": categories.get("audio"),
        "tablet": categories.get("computación"),
        "smart tv": categories.get("electrónica"),
        "mouse gamer": categories.get("computación"),
        "teclado mecanico": categories.get("computación"),
    }

    # Importar productos
    print(f"\n4. Importando productos ({len(queries)} términos de búsqueda)...")
    total_imported = 0
    total_updated = 0

    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] Buscando: '{query}'")

        try:
            # Buscar productos en Mercado Libre
            products = await ml.fetch_products(query=query, limit=limit_per_query)
            print(f"  Encontrados: {len(products)} productos")

            if not products:
                print("  ⚠️  No se encontraron productos")
                continue

            # Obtener categoría para este query
            category = query_to_category.get(query.lower())

            # Guardar cada producto
            imported = 0
            updated = 0

            for product_data in products:
                try:
                    # Buscar si ya existe (por SKU y tienda)
                    existing = None
                    if product_data.sku:
                        existing = db.query(models.Product).filter(
                            models.Product.sku == product_data.sku,
                            models.Product.store_id == store.id
                        ).first()

                    if existing:
                        # Actualizar producto existente
                        existing.name = product_data.name
                        existing.price = product_data.price
                        existing.store_url = product_data.store_url
                        existing.image_url = product_data.image_url
                        existing.available = 1 if product_data.available else 0
                        existing.currency = product_data.currency
                        existing.last_updated = datetime.utcnow()
                        updated += 1
                    else:
                        # Crear nuevo producto
                        new_product = models.Product(
                            name=product_data.name,
                            store_id=store.id,
                            category_id=category.id if category else None,
                            store_url=product_data.store_url,
                            sku=product_data.sku,
                            price=product_data.price,
                            currency=product_data.currency,
                            image_url=product_data.image_url,
                            available=1 if product_data.available else 0,
                            last_updated=datetime.utcnow()
                        )
                        db.add(new_product)
                        imported += 1

                except Exception as e:
                    print(f"    ✗ Error guardando producto: {e}")
                    continue

            # Commit batch
            try:
                db.commit()
                print(f"  ✓ Importados: {imported} | Actualizados: {updated}")
                total_imported += imported
                total_updated += updated
            except Exception as e:
                db.rollback()
                print(f"  ✗ Error en commit: {e}")

        except Exception as e:
            print(f"  ✗ Error en búsqueda '{query}': {e}")
            continue

        # Pequeño delay entre búsquedas (rate limiting)
        if i < len(queries):
            await asyncio.sleep(1)

    print("\n" + "=" * 60)
    print("RESUMEN DE IMPORTACIÓN")
    print("=" * 60)
    print(f"Productos nuevos importados: {total_imported}")
    print(f"Productos actualizados: {total_updated}")
    print(f"Total procesado: {total_imported + total_updated}")
    print("=" * 60)


async def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Importar productos desde integraciones")
    parser.add_argument(
        "--store",
        choices=["mercadolibre", "all"],
        default="mercadolibre",
        help="Tienda desde la que importar"
    )
    parser.add_argument(
        "--queries",
        type=str,
        help="Términos de búsqueda separados por comas (ej: 'laptop,iphone,tablet')"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Usar queries predefinidos"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Productos por término de búsqueda (default: 50)"
    )

    args = parser.parse_args()

    # Inicializar base de datos
    print("Inicializando base de datos...")
    init_db()

    # Determinar queries
    if args.all:
        queries = DEFAULT_QUERIES
    elif args.queries:
        queries = [q.strip() for q in args.queries.split(",")]
    else:
        queries = ["laptop", "iphone"]  # Queries por defecto

    # Crear sesión de BD
    db = SessionLocal()

    try:
        if args.store == "mercadolibre" or args.store == "all":
            await import_from_mercadolibre(db, queries, args.limit)

        # TODO: Agregar más tiendas aquí cuando estén disponibles
        # if args.store == "coppel" or args.store == "all":
        #     await import_from_coppel(db, queries, args.limit)

    finally:
        db.close()

    print("\n✓ Importación completada!")


if __name__ == "__main__":
    print("\n🚀 Iniciando importación de productos...\n")
    asyncio.run(main())
    print("\n✓ Proceso finalizado\n")
