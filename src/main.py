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

if __name__ == "__main__":
    mongo_client = get_mongo_client(CONNECTION_STRING)
    try:
        mongo_client.admin.command('ping')
        active_documents = ingest_catalog_data(mongo_client)
        print(f"[SUCCESS] Pipeline executed. Total active documents in cluster: {active_documents}")
    except Exception as error:
        print(f"[CRITICAL] Operational failure: {error}")
