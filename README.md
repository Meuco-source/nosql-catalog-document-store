# E-commerce Polymorphic Dynamic Catalog Architecture

A production-ready Data Engineering pipeline deploying an asynchronous NoSQL database architecture on MongoDB Atlas (Google Cloud Platform - Belgium Region). This system leverages a polymorphic schema layout designed to handle highly heterogeneous business inventories with zero schema rigidity.

## 🚀 Business Impact & Features
* **Polymorphic Data Modeling:** Stores diverse product catalogs (e.g., electronic hardware and specialized sporting goods) under a single collection without strict relational schema enforcement.
* **Idempotent Data Ingestion:** Implements data upsert patterns (`update_one` with `upsert=True`) ensuring structural consistency and preventing record duplication across pipeline executions.
* **Cloud-First Architecture:** Executed entirely inside isolated cloud compute resources using secure TLS/SSL handshakes via `certifi`.

## 🛠️ Tech Stack & Infrastructure
* **Engine:** MongoDB Atlas Cloud NoSQL
* **Language:** Python 3.11+
* **Driver:** PyMongo (`pymongo[srv]`)
* **Environment:** Fully cloud-managed (Google Colab / GitHub Codespaces compatible)

## 📊 Sample Ingested Document Structure (BSON/JSON)
```json
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
  }
}
