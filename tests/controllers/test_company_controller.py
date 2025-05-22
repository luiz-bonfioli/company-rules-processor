from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.controllers.company_controller import router
from src.core.context import get_company_service


@pytest.fixture
def mock_company_service():
    service = MagicMock()
    service.import_data.return_value = {"imported": 3, "failed": 0}
    service.import_file = AsyncMock(return_value={"imported": 2, "failed": 1})
    service.process_company.return_value = [{"url": "https://example.com", "status": "processed"}]
    service.get_companies_previously_processed.return_value = {"companies": []}
    return service


@pytest.fixture
def test_app(mock_company_service):
    app = FastAPI()
    app.dependency_overrides[get_company_service] = lambda: mock_company_service
    app.include_router(router)
    return app


def test_import_company_data_invalid_content_type(test_app):
    client = TestClient(test_app)

    headers = {"content-type": "text/plain"}
    response = client.post("/v1/company/import-company-data", content="invalid", headers=headers)

    assert response.status_code == 415


def test_process_company(test_app):
    client = TestClient(test_app)

    payload = {
        "urls": ["https://example.com"],
        "rules": []
    }

    response = client.post("/v1/company/process-company", json=payload)

    assert response.status_code == 200
    assert response.json() == [{"url": "https://example.com", "status": "processed"}]


def test_get_companies(test_app):
    client = TestClient(test_app)

    response = client.get("/v1/company/get-companies")

    assert response.status_code == 200
    assert response.json() == {"companies": []}
