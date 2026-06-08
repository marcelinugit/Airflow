# 🚀 PostgreSQL Data Ingestion Pipeline with Apache Airflow

This project simulates a real-world Data Engineering workflow using PostgreSQL, Docker, Apache Airflow and Python.

The pipeline extracts data from a PostgreSQL database, processes it using Pandas, and stores the results in CSV or Parquet files through an orchestrated Airflow DAG.

---

# 🎯 Project Goal

Build an end-to-end ingestion pipeline that demonstrates:

* PostgreSQL provisioning with Docker
* Persistent database storage using Docker Volumes
* Workflow orchestration with Apache Airflow
* Data extraction from PostgreSQL
* Data transformation using Pandas
* Data persistence in CSV or Parquet format
* Execution monitoring and logging

---

# 🏗️ Architecture

PostgreSQL (Docker)

↓

Apache Airflow

↓

Extract

↓

Transform (Pandas)

↓

Load

↓

CSV / Parquet Files

---

# 🛠️ Technologies

* Python
* Apache Airflow
* PostgreSQL
* Docker
* Pandas
* PyArrow
* Docker Compose

---

# 📦 Project Features

* PostgreSQL containerized with Docker
* Persistent storage using Docker Volumes
* Automatic database initialization through SQL scripts
* Airflow DAG orchestration
* PostgreSQL connection validation
* Data extraction from multiple tables
* DataFrame processing with Pandas
* Export to CSV or Parquet
* Execution logs and metrics

---

# 📂 Dataset

The project uses two sample tables:

## usuario

* id
* nome
* email
* data_criacao

## produto

* id
* nome
* preco
* data_criacao

---

# 📁 Project Structure

dags/
├── ingestao_postgres.py

sql/
├── init.sql

data/
└── landing/
├── usuario.parquet
└── produto.parquet

docker-compose.yml

README.md

---

# 🔄 ETL Flow

Extract

* Read data from PostgreSQL
* Execute SQL queries

Transform

* Convert query results into Pandas DataFrames
* Validate schema
* Validate record counts

Load

* Save data to CSV or Parquet files

---

# 📊 Logging

The pipeline records:

* Execution timestamp
* Number of records extracted
* Processing duration
* Execution status

---

# ✅ Validation

* PostgreSQL container running
* Volume persistence validated
* Airflow connection working
* DAG executed successfully
* Files generated in landing layer
* Data preserved after container restart

---

# 📚 Learning Objectives

This project was built to practice:

* Docker Networking
* Docker Volumes
* PostgreSQL administration
* Apache Airflow fundamentals
* DAGs and Task orchestration
* ETL development
* Data Engineering workflows
* Production-like data pipelines
