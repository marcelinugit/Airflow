# 🐍 MySQL ETL Pipeline (Python)

This project was built as part of my learning journey to become a Software Engineer / Data Engineer, focusing on building real-world ETL pipelines using Python and MySQL.

A simple ETL pipeline built with Python that extracts data from a MySQL database and exports it to CSV files.

---

# 💡 Motivation

This project simulates a real ETL pipeline used in data engineering systems, where data is extracted from a database, processed, and stored in a structured format for further analysis.

It was built to practice:
- Clean Architecture
- Separation of Responsibilities
- Dependency Injection
- ETL concepts (Extract → Transform → Load)

---

# 🚀 Features

- Connects to MySQL database
- Executes SQL queries
- Transforms results into structured data (`list[dict]`)
- Exports data to CSV files
- Environment-based configuration (`.env`)
- Modular and scalable architecture

---

# 🛠️ Tech Stack

- Python
- MySQL
- python-dotenv

---

# 🏗️ Project Structure

src/
├── clients/        # MySQL connection layer
├── config/         # Environment settings (.env loader)
├── jobs/           # ETL pipeline logic
└── main.py         # Application entry point

tests/              # Unit tests
bucket/             # Output CSV files

---

# ⚙️ How it works

Data flows through the pipeline:

MySQL Database → MySQLClient → ETL Job → CSV File (bucket/)

---

# 🔧 Setup

## 1. Clone repository

git clone https://github.com/your-username/mysql-etl-pipeline-python.git  
cd mysql-etl-pipeline-python  

## 2. Create virtual environment

python -m venv venv  

Activate:

Windows:
venv\Scripts\activate  

Linux/Mac:
source venv/bin/activate  

## 3. Install dependencies

pip install -r requirements.txt  

---

# 🔐 Environment Variables (.env)

Create a `.env` file in the root folder:

MYSQL_HOST=localhost  
MYSQL_USER=your_user  
MYSQL_PASSWORD=your_password  
MYSQL_DATABASE=your_database  

OUTPUT_PATH=./bucket  

---

# ▶️ Run the project

python src/main.py  

---

# 🧠 Architecture Highlights

This project applies:
- Single Responsibility Principle (SRP)
- Dependency Injection
- Separation of Concerns
- Modular design
- Reusable components

---

# 📦 Output

After execution, CSV files will be generated in:

bucket/

---

# 📚 Learning Focus

This project was built to practice:
- Python OOP
- MySQL integration
- ETL pipelines
- Clean code principles
- Software architecture fundamentals

---

# 🚧 Future Improvements

- Add logging system
- Add unit tests coverage
- Add data validation layer
- Support multiple tables extraction
- Docker support
- CI/CD pipeline (GitHub Actions)

---

# 👨‍💻 Author

Built by Gustavo Marcelino — aspiring Software Engineer focused on Python, Data Engineering and Backend systems.