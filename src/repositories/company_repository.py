import json
from datetime import datetime
from typing import Any

from src.core.database.database import Database
from src.core.database.schema import UPSERT_DATA_IN_BATCH, SELECT_COMPANY_BY_URL, UPDATE_PROCESSED_DATA, \
    SELECT_PREVIOUSLY_PROCESSED


class CompanyRepository:

    def __init__(self, db: Database):
        self.__db = db

    def upsert_data(self, data: list[dict[str, Any]]):
        values = [
            (row["url"],
             row["company_name"],
             json.dumps(row),
             None,
             datetime.now(),
             None)
            for row in data
        ]
        return self.__db.execute_insert_many(UPSERT_DATA_IN_BATCH, values)

    def upsert_processed_data(self, url: str, last_processed_date: datetime, processed: dict[str, Any]):
        values = (json.dumps(processed),
                  last_processed_date,
                  url)
        return self.__db.execute(UPDATE_PROCESSED_DATA, values)

    def fetch_by_url(self, url: str):
        return self.__db.fetch_one(SELECT_COMPANY_BY_URL, (url,))

    def get_companies_previously_processed(self):
        return self.__db.fetch_all(SELECT_PREVIOUSLY_PROCESSED)

