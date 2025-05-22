import json
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.core.database.schema import UPSERT_DATA_IN_BATCH, UPDATE_PROCESSED_DATA, SELECT_COMPANY_BY_URL, \
    SELECT_PREVIOUSLY_PROCESSED
from src.repositories.company_repository import CompanyRepository


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def repo(mock_db):
    return CompanyRepository(mock_db)


def test_upsert_data(repo, mock_db):
    now = datetime.now()
    data = [{
        "url": "https://example.com",
        "company_name": "Example Inc."
    }]

    repo.upsert_data(data)
    expected_values = [(
        "https://example.com",
        "Example Inc.",
        json.dumps(data[0]),
        None,
        mock_db.execute_insert_many.call_args[0][1][0][4],
        None
    )]

    call_args = mock_db.execute_insert_many.call_args[0]
    assert call_args[0] == UPSERT_DATA_IN_BATCH


def test_upsert_processed_data(repo, mock_db):
    processed = {"score": 0.95}
    timestamp = datetime.now()
    url = "https://example.com"

    repo.upsert_processed_data(url, timestamp, processed)

    mock_db.execute.assert_called_once_with(
        UPDATE_PROCESSED_DATA,
        (json.dumps(processed), timestamp, url)
    )


def test_fetch_by_url(repo, mock_db):
    url = "https://example.com"
    repo.fetch_by_url(url)
    mock_db.fetch_one.assert_called_once_with(SELECT_COMPANY_BY_URL, (url,))


def test_get_companies_previously_processed(repo, mock_db):
    repo.get_companies_previously_processed()
    mock_db.fetch_all.assert_called_once_with(SELECT_PREVIOUSLY_PROCESSED)
