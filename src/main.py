import pymongo
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

CONNECTION_STRING = "mongodb+srv://admin_data:RO6AG5bVP0Q2b7q@cluster0.caydb8p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_mongo_client(uri: str) -> MongoClient:
    """Initializes a secure MongoClient instances with TLS validation."""
    return MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

def ingest_catalog_data(client: MongoClient) -> int:
    """Ingests polymorphic e-commerce documents into the production cluster."""
    db = client["ecommerce_platform"]
    products_collection = db["products"]
    
    catalog_data = [
        {
            "sku": "TECH-X1-MK3",
            "name": "Traktor Kontrol X1 MK3",
            "category": "Electronics",
            "price": 299.00,
            "stock": 15,
            "specs": {
                "connectivity": "USB-C Hub",
                "displays": "OLED Screens",
                "tactile_controls": 34
            }
        },
        {
            "sku": "SNOW-BRTN-CSTM",
            "name": "Burton Custom V-Rocker Snowboard",
            "category": "Sporting Goods",
            "price": 620.00,
            "stock": 8,
            "specs": {
                "profile": "V-Rocker",
                "shape": "Directional",
                "terrain": ["All-Mountain", "Powder"]
            },
            "tags": ["Rocker", "Channel-System"]
        }
    ]
    
    for product in catalog_data:
        products_collection.update_one(
            {"sku": product["sku"]}, 
            {"$set": product}, 
            upsert=True
        )
    return products_collection.count_documents({})

def query_electronics_catalog(client: MongoClient):
    """Queries and filters products under the electronics category with specific projections."""
    db = client["ecommerce_platform"]
    products_collection = db["products"]
    
    print("\n--- [QUERY] Fetching Electronics with Embedded Specifications ---")
    # Filtramos por categoría y proyectamos solo campos necesarios para optimizar ancho de banda
    query = {"category": "Electronics"}
    projection = {"name": 1, "price": 1, "specs.displays": 1, "_id": 0}
    
    results = products_collection.find(query, projection)
    for doc in results:
        print(f"Product: {doc.get('name')} | Price: ${doc.get('price')} | UI: {doc.get('specs', {}).get('displays', 'N/A')}")

def query_low_stock_alerts(client: MongoClient, threshold: int = 10):
    """Fetches items with stock levels below the specified threshold."""
    db = client["ecommerce_platform"]
    products_collection = db["products"]
    
    print(f"\n--- [QUERY] Inventory Alert: Stock lower than {threshold} units ---")
    query = {"stock": {"$lt": threshold}}
    
    results = products_collection.find(query)
    for doc in results:
        print(f"ALERT -> SKU: {doc.get('sku')} | Name: {doc.get('name')} | Current Stock: {doc.get('stock')}")

def query_electronics_catalog(client: MongoClient):
    """Queries and filters products under the electronics category with specific projections."""
    db = client["ecommerce_platform"]
    products_collection = db["products"]
    
    print("\n--- [QUERY] Fetching Electronics with Embedded Specifications ---")
    # Filtramos por categoría y proyectamos solo campos necesarios para optimizar ancho de banda
    query = {"category": "Electronics"}
    projection = {"name": 1, "price": 1, "specs.displays": 1, "_id": 0}
    
    results = products_collection.find(query, projection)
    for doc in results:
        print(f"Product: {doc.get('name')} | Price: ${doc.get('price')} | UI: {doc.get('specs', {}).get('displays', 'N/A')}")

def query_low_stock_alerts(client: MongoClient, threshold: int = 10):
    """Fetches items with stock levels below the specified threshold."""
    db = client["ecommerce_platform"]
    products_collection = db["products"]
    
    print(f"\n--- [QUERY] Inventory Alert: Stock lower than {threshold} units ---")
    query = {"stock": {"$lt": threshold}}
    
    results = products_collection.find(query)
    for doc in results:
        print(f"ALERT -> SKU: {doc.get('sku')} | Name: {doc.get('name')} | Current Stock: {doc.get('stock')}")

if __name__ == "__main__":
    mongo_client = get_mongo_client(CONNECTION_STRING)
    try:
        mongo_client.admin.command('ping')
        active_documents = ingest_catalog_data(mongo_client)
        print(f"[SUCCESS] Pipeline executed. Total active documents: {active_documents}")
        
        # Ejecución de consultas analíticas avanzadas
        query_electronics_catalog(mongo_client)
        query_low_stock_alerts(mongo_client, threshold=10)
        
    except Exception as error:
        print(f"[CRITICAL] Operational failure: {error}")
