# 🏢 Enterprise Lead Gen Platform

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![SQLite](https://img.shields.io/badge/database-SQLite-green.svg)]()
[![Docker](https://img.shields.io/badge/deployment-Docker-blue.svg)]()

## 📌 Overview
An automated, high-throughput B2B lead generation pipeline. This system intelligently crawls localized data sources, enriches them via external APIs (e.g., Google Maps), and structures the output into a relational database.

It perfectly demonstrates **data flows, API integration, and database management** — core requirements for modern backend and AI-integrated data systems.

## 🏗️ Architecture
* **`smart_crawler.py`**: The core ingestion engine. Implements rate-limiting, error handling, and robust data extraction logic to prevent IP bans and handle malformed HTML/JSON.
* **`google_maps_api.py`**: The enrichment layer. Takes raw business data and augments it with geographical and contact information via external APIs.
* **`leads.db`**: SQLite database acting as the single source of truth, ensuring ACID compliance for the scraped data.
* **`auto_run.py` & `main.py`**: The orchestration layer. Manages the lifecycle of the data pipeline.

## 🚀 Key Features
* **Resilient Data Pipelines:** The crawler is built to handle network failures and API rate limits gracefully.
* **Relational Database Design:** Normalizes incoming chaotic data into structured SQL tables.
* **Dockerized Execution:** Completely reproducible environment.

## ⚙️ How to Run (Docker)
```bash
docker build -t enterprise-lead-gen .
docker run --env-file .env -v $(pwd)/leads.db:/app/leads.db enterprise-lead-gen
```
*(Note: Uses volume mapping to persist the SQLite database outside the container)*
