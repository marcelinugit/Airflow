# 🚀 PostgreSQL Data Ingestion Pipeline with Apache Airflow

## 📖 Overview

This project demonstrates an end-to-end data ingestion workflow using PostgreSQL, Apache Airflow, Docker, and Pandas.

The pipeline extracts data from a PostgreSQL database, processes the data into Pandas DataFrames, and stores the results as CSV or Parquet files. The entire workflow is orchestrated through an Airflow DAG.

---

## 🎯 Project Goals

* Provision PostgreSQL using Docker
* Configure persistent storage with Docker Volumes
* Create and populate sample tables automatically
* Connect Airflow to PostgreSQL
* Extract data from PostgreSQL
* Transform data using Pandas
* Store processed data in CSV or Parquet format
* Monitor execution through Airflow logs

---

## 🏗️ Architecture

```text
PostgreSQL (Docker)
          │
          ▼
Apache Airflow
          │
          ▼
      Extract
          │
          ▼
     Transform
      (Pandas)
          │
          ▼
         Load
          │
          ▼
 CSV / Parquet Files
```

---

## 🛠️ Tech Stack

* Python
* Apache Airflow
* PostgreSQL
* Docker
* Docker Compose
* Pandas
* PyArrow

---

## 📂 Dataset

### Table: usuario

| Column       | Type      |
| ------------ | --------- |
| id           | SERIAL    |
| nome         | VARCHAR   |
| email        | VARCHAR   |
| data_criacao | TIMESTAMP |

### Table: produto

| Column       | Type      |
| ------------ | --------- |
| id           | SERIAL    |
| nome         | VARCHAR   |
| preco        | NUMERIC   |
| data_criacao | TIMESTAMP |

---

## 📁 Project Structure

```text
.
├── dags/
│   └── postgres_ingestion_dag.py
│
├── sql/
│   └── init.sql
│
├── data/
│   └── landing/
│       ├── users.parquet
│       └── products.parquet
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔄 ETL Flow

### Extract

* Connect to PostgreSQL
* Read data from:

  * usuario
  * produto

### Transform

* Convert query results into Pandas DataFrames
* Validate schemas
* Validate record counts

### Load

* Save datasets as:

  * CSV files
  * Parquet files

---

## 📊 Logging

The pipeline records:

* Execution timestamp
* Number of records extracted
* Processing duration
* Execution status

---

## ⚙️ Features

* PostgreSQL running in Docker
* Persistent data storage using Docker Volumes
* Automatic database initialization via SQL scripts
* Airflow DAG orchestration
* PostgreSQL connection validation
* Data extraction from multiple tables
* Pandas-based transformations
* CSV and Parquet export
* Execution monitoring and logging

---

## ✅ Validation

The project validates:

* PostgreSQL container creation
* Persistent storage functionality
* Automatic execution of initialization scripts
* Airflow ↔ PostgreSQL connectivity
* Successful DAG execution
* Output file generation
* Data persistence after container restart

---

## 📚 Learning Objectives

This project was built to practice:

* Docker Containers
* Docker Networks
* Docker Volumes
* PostgreSQL
* Apache Airflow
* DAGs and Task Orchestration
* ETL Development
* Pandas
* Data Engineering Fundamentals

---

## 🎓 Project Context

This project was developed as part of a Data Engineering learning journey, focusing on workflow orchestration, database integration, containerization, and ETL pipeline development using industry-standard tools.
