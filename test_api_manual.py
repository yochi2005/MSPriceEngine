"""Test manual de la API."""
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, init_db
from app import models

# Inicializar BD
init_db()

# Crear cliente de prueba
client = TestClient(app)

print("="*60)
print("PRUEBAS DE LA API - MSPriceEngine")
print("="*60)

# Test 1: Root endpoint
print("\n1. Test: GET / (Root)")
response = client.get("/")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
assert response.status_code == 200

# Test 2: Health check
print("\n2. Test: GET /health")
response = client.get("/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
assert response.status_code == 200

# Test 3: Get stores (debería estar vacío)
print("\n3. Test: GET /stores")
response = client.get("/stores")
print(f"   Status: {response.status_code}")
print(f"   Stores found: {len(response.json())}")
assert response.status_code == 200

# Test 4: Crear tienda de prueba
print("\n4. Test: Creando tienda de prueba en BD...")
db = SessionLocal()
store = models.Store(name="Amazon MX Test", url="https://amazon.com.mx")
db.add(store)
db.commit()
db.refresh(store)
print(f"   ✓ Store created: ID={store.id}, Name={store.name}")

# Test 5: Crear producto de prueba
print("\n5. Test: Creando producto de prueba...")
product = models.Product(
    name="Laptop HP Pavilion Gaming 15",
    store_id=store.id,
    store_url="https://amazon.com.mx/dp/TEST123",
    sku="TEST123",
    price=12999.99,
    currency="MXN",
    available=1
)
db.add(product)
db.commit()
db.refresh(product)
print(f"   ✓ Product created: ID={product.id}, Name={product.name}, Price=${product.price}")

# Test 6: Buscar producto vía API
print("\n6. Test: GET /search?q=laptop")
response = client.get("/search?q=laptop")
print(f"   Status: {response.status_code}")
data = response.json()
print(f"   Total results: {data['total']}")
if data['products']:
    print(f"   First product: {data['products'][0]['name']} - ${data['products'][0]['price']}")
assert response.status_code == 200
assert data['total'] >= 1

# Test 7: Get product by ID
print("\n7. Test: GET /products/{product_id}")
response = client.get(f"/products/{product.id}")
print(f"   Status: {response.status_code}")
prod_data = response.json()
print(f"   Product: {prod_data['name']}")
print(f"   Store: {prod_data['store']['name']}")
assert response.status_code == 200

# Test 8: Search con filtros
print("\n8. Test: GET /search?q=laptop&min_price=10000&max_price=15000")
response = client.get("/search?q=laptop&min_price=10000&max_price=15000")
print(f"   Status: {response.status_code}")
data = response.json()
print(f"   Results with price filter: {data['total']}")
assert response.status_code == 200

# Test 9: Paginación
print("\n9. Test: GET /search?q=laptop&limit=1")
response = client.get("/search?q=laptop&limit=1")
data = response.json()
print(f"   Total: {data['total']}, Returned: {len(data['products'])}")
assert len(data['products']) <= 1

# Cleanup
print("\n10. Cleanup: Eliminando datos de prueba...")
db.delete(product)
db.delete(store)
db.commit()
db.close()

print("\n" + "="*60)
print("✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
print("="*60)
