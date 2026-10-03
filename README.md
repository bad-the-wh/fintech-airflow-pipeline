# Fintech Crypto Market ETL Pipeline

A production-grade, containerized Airflow ETL pipeline designed for fintech analytics. This system extracts live cryptocurrency market data, performs rigorous data sanitization, validates structural and financial constraints, and loads clean records into a relational database.

---

## 🏗️ Architecture & Workflow

The pipeline runs as an orchestrated Directed Acyclic Graph (DAG) with the following stages:

1. **Extract (`extract_market_data`)**: Pulls current market metrics (prices, volumes, market caps) via public APIs (e.g., CoinGecko).
2. **Transform (`transform_market_data`)**: Normalizes tickers, handles null/missing values, parses timestamps, and injects corporate auditing metadata (`etl_transformed_at`).
3. **Data Quality Gate (`run_data_quality_validations`)**: Evaluates records against strict assertions (primary key existence, negative price checks) to prevent corrupted data from hitting production tables.
4. **Load (`load_market_data`)**: Persists the clean, validated dataset into PostgreSQL.

---

## 🛠️ Tech Stack

* **Orchestration**: Apache Airflow (TaskFlow API decorators)
* **Data Processing**: Pandas, NumPy
* **Database**: PostgreSQL (via SQLAlchemy / Airflow Hooks)
* **Language**: Python 3.10+
* **Environment**: Containerized execution environment

---

## 📂 Project Structure

```text
fintech_crypto_market_etl/
│
├── dags/
│   └── crypto_market_dag.py        # Main Airflow DAG definition & failure alerts
├── include/
│   ├── extract.py                  # API extraction logic
│   ├── transform.py                # Data cleaning & type enforcement
│   ├── data_quality.py             # Validation checks & assertions
│   └── load.py                     # Database loading module
├── logs/                           # Airflow task execution logs
└── README.md