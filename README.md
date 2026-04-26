# Data-Stock ↗

**Data-Stock** is a robust, secure, and highly scalable backend system designed for intelligent inventory control in large-scale enterprises. It provides real-time visibility into stock movements across multiple warehouses, automated alerts for stockouts, and advanced analytical reporting.

---

## 🚀 Key Features

- **🔐 Enterprise-Grade Security:** Full implementation of JWT (JSON Web Tokens) for secure authentication and authorization. Password hashing using `bcrypt`.
- **🏢 Multi-Warehouse Support:** Advanced inventory management allowing the same SKU to be tracked independently across multiple storage locations.
- **⚡ Real-Time Stock Logic:** Intelligent processing of entries and exits with transactional integrity.
- **🚨 Automated Alerts:** Real-time generation of "Low Stock" and "Rupture" alerts based on configurable minimum levels.
- **📊 Advanced Analytics:** High-performance data processing using **Pandas** for turnover reports, warehouse utilization, and stock health summaries.
- **⚙️ Data Orchestration:** Integrated with **Apache Airflow** for scheduled reporting and batch data processing.
- **🐳 Containerized:** Fully Dockerized environment for seamless deployment and development.

---

## 🛠 Tech Stack

- **Backend:** [Python 3.11+](https://www.python.org/)
- **API Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database / ORM:** [PostgreSQL](https://www.postgresql.org/) & [SQLModel](https://sqlmodel.tiangolo.com/)
- **Analytics:** [Pandas](https://pandas.pydata.org/)
- **Orchestration:** [Apache Airflow](https://airflow.apache.org/)
- **Infrastructure:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## 📂 Project Structure

```text
data-stock/
├── app/
│   ├── api/             # FastAPI Routers & Endpoints
│   ├── core/            # Configuration, Security, and Database Logic
│   ├── models/          # SQLModel Database Entities
│   ├── schemas/         # Pydantic Schemas for API Requests/Responses
│   ├── services/        # Business Logic & Analytics (Stock/Pandas)
│   └── main.py          # Application Entry Point
├── airflow/             # Airflow DAGs and Configuration
├── tests/               # Pytest Suite
├── Dockerfile           # FastAPI Container Config
└── docker-compose.yml   # Multi-service Orchestration
```

---

## 🚦 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ruok-dev/data-stock.git
cd data-stock
```

### 2. Configure Environment
Copy the example environment file and fill in your secrets:
```bash
cp .env.example .env
```

### 3. Run with Docker
```bash
docker-compose up --build
```

### 4. Access the API
- **Swagger Documentation:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🧪 Testing

Run the automated test suite using `pytest`:
```bash
source .venv/bin/activate
PYTHONPATH=. pytest tests/
```

---

## 🛡 Security First

- **Zero Hardcoded Secrets:** All configuration is strictly environment-based.
- **Safe Defaults:** Production-ready settings for JWT and CORS.
- **Data Integrity:** Transactional movements to prevent stock inconsistencies.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
