import json
from typing import Any

from src.core.database.database import Database
from src.core.database.schema import UPSERT_DATA_IN_BATCH, SELECT_COMPANY_BY_URL


class CompanyRepository:

    def __init__(self, db: Database):
        self.__db = db

    def upsert_data(self, data: list[dict[str, Any]]):
        values = [
            (row["url"], row["company_name"], json.dumps(row))
            for row in data
        ]
        return self.__db.execute_insert_many(UPSERT_DATA_IN_BATCH, values)

    def fetch_by_url(self, url: str):
        return self.__db.fetch_one(SELECT_COMPANY_BY_URL, (url,))
