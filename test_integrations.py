"""
Script de prueba para las nuevas integraciones.

Prueba la integración de Mercado Libre como ejemplo.
"""
import asyncio
from app.integrations.stores.mercadolibre import MercadoLibreIntegration


async def test_mercadolibre():
    """Probar integración de Mercado Libre."""
    print("=" * 60)
    print("PROBANDO INTEGRACIÓN DE MERCADO LIBRE")
    print("=" * 60)

    # Inicializar
    ml = MercadoLibreIntegration()

    # 1. Probar conexión
    print("\n1. Probando conexión...")
    connected = await ml.test_connection()
    print(f"   ✓ Conexión exitosa: {connected}")

    if not connected:
        print("   ✗ No se pudo conectar a Mercado Libre")
        return

    # 2. Buscar productos
    print("\n2. Buscando productos: 'laptop'...")
    products = await ml.fetch_products(query="laptop", limit=5)
    print(f"   ✓ Productos encontrados: {len(products)}")

    # 3. Mostrar resultados
    print("\n3. Primeros 5 productos:")
    print("-" * 60)
    for i, p in enumerate(products, 1):
        print(f"\n   [{i}] {p.name}")
        print(f"       Precio: ${p.price:,.2f} {p.currency}")
        print(f"       Tienda: {p.store_name}")
        print(f"       SKU: {p.sku}")
        print(f"       Disponible: {'Sí' if p.available else 'No'}")
        print(f"       URL: {p.store_url}")
        print(f"       Imagen: {p.image_url[:60]}...")
        if p.category:
            print(f"       Categoría: {p.category}")

    # 4. Probar con límite mayor
    print("\n4. Probando búsqueda con más resultados (50)...")
    products_large = await ml.fetch_products(query="iphone", limit=50)
    print(f"   ✓ Productos encontrados: {len(products_large)}")

    # 5. Obtener categorías disponibles
    print("\n5. Obteniendo categorías de Mercado Libre...")
    categories = await ml.get_categories()
    print(f"   ✓ Categorías disponibles: {len(categories)}")
    print("\n   Primeras 10 categorías:")
    for cat in categories[:10]:
        print(f"   - {cat['id']}: {cat['name']}")

    print("\n" + "=" * 60)
    print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)


async def test_feeds():
    """Probar parsers de feeds (requiere configuración)."""
    from app.integrations.stores.coppel import CoppelIntegration
    from app.integrations.stores.sears import SearsIntegration

    print("\n" + "=" * 60)
    print("PROBANDO INTEGRACIONES DE FEEDS")
    print("=" * 60)

    # Nota: Estas integraciones requieren URLs de feeds configuradas
    print("\n⚠️  Coppel y Sears requieren configuración de feed_url")
    print("   Ver docs/INTEGRATION_GUIDE.md para más información")

    # Ejemplo de configuración (URLs ficticias)
    # coppel_config = {
    #     'feed_url': 'https://coppel.com/api/products.json'
    # }
    # coppel = CoppelIntegration(config=coppel_config)
    # products = await coppel.fetch_products(query="laptop")


async def main():
    """Ejecutar todas las pruebas."""
    try:
        # Probar Mercado Libre
        await test_mercadolibre()

        # Probar feeds (requiere configuración)
        await test_feeds()

    except Exception as e:
        print(f"\n✗ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🚀 Iniciando pruebas de integraciones...\n")
    asyncio.run(main())
    print("\n✓ Pruebas finalizadas\n")
