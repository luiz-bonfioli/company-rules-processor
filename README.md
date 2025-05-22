# Company Rules Processor

A Python API to process company data based on dynamic, customizable rules.

---

## Features

- Upload company datasets via CSV or JSON
- Dynamically apply custom rules to process data
- Lightweight and container-ready
- Health and status endpoints for monitoring

---

## Requirements

- Python 3.11
- pip for dependency management
- PostgreSQL (for data persistence)
- Docker (optional, for containerized usage)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/luiz-bonfioli/company-rules-processor.git
cd company-rules-processor
```

### 2. Install Pip (if needed)

```bash
python -m ensurepip --upgrade
```

### 3. Install PostgreSQL (MacOS example using Homebrew)

```bash
brew install postgresql
```

### 4. Create and Activate a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Install PyTest for tests

```bash
pip install pytest
```

---

## Run with Docker

You can run the application using Docker for easier setup.

### Build Docker Image

```bash
docker build -t company-rules-processor .
```

### Run unit tests

```bash
pytest tests/
```



### Start Services

```bash
docker-compose up -d
```

---

## Example API Usage

### Upload Company Data (CSV)

```bash
curl -i -X POST http://localhost:8080/v1/company/import-company-data \
  -F "file=@./assets/company-dataset.csv"
```

### Upload Company Data (JSON)

```bash
curl -i -X POST http://localhost:8080/v1/company/import-company-data \
  -H "Content-Type: application/json" \
  -d '[
        {
          "url": "https://www.nexuswave.tech",
          "is_saas": false,
          "industry": "Software Development",
          "company_age": 6,
          "description": "Application development environment with seamless deployment across platforms, annual licensing and implementation services",
          "company_name": "NexusWave Systems",
          "founded_year": "2019",
          "is_usa_based": false,
          "total_employees": "52",
          "employee_rowth_2Y": "61.5",
          "headquarters_city": "Toronto (Canada)",
          "employee_growth_1Y": "26.7",
          "employee_growth_6M": "14.2",
          "employee_locations": "{\"USA\": 15, \"Canada\": 31, \"UK\": 3, \"India\": 2, \"Brazil\": 1}"
       }
    ]'
```


### Process Company data based on Rules

```bash
curl -i -X POST http://localhost:8080/v1/company/process-company \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://www.cloudlogiclabs.com",
      "https://www.datasynctech.io",
      "https://www.cloudops.tech",
      "https://www.secureedgesolutions.com"
    ],
    "rules": [
      {
        "input": "total_employees",
        "feature_name": "head_count_feature",
        "operation": { "greater_than": 80 },
        "match": 0,
        "default": 1
      },
      {
        "input": "company_age",
        "feature_name": "age_feature",
        "operation": { "less_than": 10 },
        "match": 1,
        "default": 0
      },
      {
        "input": "is_usa_based",
        "feature_name": "usa_based_feature",
        "operation": { "equal": true },
        "match": 1,
        "default": 0
      },
      {
        "input": "is_saas",
        "feature_name": "is_saas_feature",
        "operation": { "equal": true },
        "match": 1,
        "default": 0
      }
    ]
  }'

```

### Get All Companies

```bash
curl -i -X GET http://localhost:8080/v1/company/get-companies
```

### Check Status Endpoint

```bash
curl -i -X GET http://localhost:8080/status
```
Response:
```
{
  "status": "ok",
  "timestamp": "2025-05-22 15:45:56.407350",
  "dependencies": {
    "database": "ok"
  }
}
```

### Check Health Endpoint

```bash
curl -i -X GET http://localhost:8080/health
```
Response
```
{
  "status": "ok"
}
```

---

## Project Structure

```bash
.
├── src/                     # Main application code
├── assets/                  # Assets 
├── tests/                   # Unit and integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

