import os
import pymongo
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# ============================================================================
# 1. SEGURIDAD E INFRAESTRUCTURA DE RED (Aislamiento de credenciales)
# ============================================================================
CONNECTION_STRING = os.getenv(
    "MONGO_CONNECTION_STRING", 
    "mongodb+srv://admin_data:RO6AG5bVP0Q2b7q@cluster0.caydb8p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

def get_mongo_client(uri: str) -> MongoClient:
    """Initializes a secure MongoClient instance with TLS validation and Server API v1."""
    return MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# ============================================================================
# 2. PIPELINE DE INGESTA (Idempotencia en Catálogo Polimórfico)
# ============================================================================
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

# ============================================================================
# 3. CAPA ANALÍTICA AVANZADA (Aggregation Framework)
# ============================================================================
def run_inventory_analytics(client: MongoClient):
    """Executes a multi-stage aggregation pipeline to compute inventory financial KPIs."""
    db = client["ecommerce_platform"]
    products_collection = db["products"]
    
    print("\n--- [ANALYTICS] Executing Multi-Stage Aggregation Pipeline ---")
    
    # Canalización de etapas: Proyección matemática y agrupación financiera
    pipeline = [
        {
            "$project": {
                "category": 1,
                "sku": 1,
                "inventory_value": {"$multiply": ["$price", "$stock"]}
            }
        },
        {
            "$group": {
                "_id": "$category",
                "total_value": {"$sum": "$inventory_value"},
                "unique_products": {"$sum": 1}
            }
        },
        {
            "$sort": {"total_value": -1}
        }
    ]
    
    results = products_collection.aggregate(pipeline)
    for report in results:
        print(f"Category: {report['_id']} | Total Value: ${report['total_value']:.2f} | SKUs: {report['unique_products']}")

if __name__ == "__main__":
    mongo_client = get_mongo_client(CONNECTION_STRING)
    try:
        mongo_client.admin.command('ping')
        print("[SUCCESS] Infrastructure Connected to Cloud Server.")
        
        # Ejecutar carga de datos
        active_documents = ingest_catalog_data(mongo_client)
        print(f"[SUCCESS] Pipeline executed. Total active documents: {active_documents}")
        
        # Ejecutar métricas financieras en la nube
        run_inventory_analytics(mongo_client)
        
    except Exception as error:
        print(f"[CRITICAL] Operational failure under execution: {error}")
