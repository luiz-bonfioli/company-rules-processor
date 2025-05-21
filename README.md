# A Python API to process company data based on dynamic rules


## Requirements

- Python 3.11
- Pip (for dependency management)

## Installation

To get started with this project, you'll need to have pip installed. If you don't have pip installed yet, you can install it by following these steps:

### Install Pip

You can install Pip using the following command:

```bash
python -m ensurepip --upgrade
```

### Install Postgresql
```bash
brew install postgresql
```

### Configure venv
```bash
python -m venv .venv
```

### Activate venv
```bash
 source .venv/bin/activate
```

### Install Dependencies

```bash
 pip install -r requirements.txt
```

### Install infra (postgres)
```bash
cd infra
```
```bash
docker-compose up -d
```

```
curl -i -X POST http://localhost:8080/v1/company/import-company-data \
  -F "file=@./company-dataset.csv"
```
```
curl -i -X POST http://localhost:8080/v1/company/import-company-data \
  -H "Content-Type: application/json" \
  -d '{"foo": "bar", "baz": 123}'
```

