# E-commerce Polymorphic Dynamic Catalog Architecture

![Automated Ingestion Status](https://github.com/Meuco-source/nosql-catalog-document-store/workflows/Automated%20NoSQL%20Data%20Ingestion%20Pipeline/badge.svg)
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
## 📊 Advanced Analytics & Data Querying
The pipeline includes analytical querying layers utilizing MongoDB’s query operators:
* **Selective Projection:** Filters complex nested documents (e.g., retrieving `specs.displays` for audio hardware) minimizing network payload sizes.
* **Range-based Evaluation:** Leverages operators like `$lt` (less than) to trigger automated low-stock supply chain alerts.
## ⚙️ CI/CD & Data Orchestration
The data ingestion and analytical layer are fully automated using **GitHub Actions**:
* **Scheduled Trigger:** Configured via a `cron` schedule to execute automatically every Monday at 08:00 UTC for automated inventory updates.
* **Secret Masking:** Database credentials are systematically isolated from the source code, leveraging GitHub's encrypted secrets framework (`secrets.MONGO_CONNECTION_STRING`).
