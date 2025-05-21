import json
import uuid
from typing import Any

from src.core.database.database import Database
from src.core.database.schema import UPSERT_DATA_IN_BATCH


class CompanyRepository:

    def __init__(self, db: Database):
        self.__db = db

    def upsert_data(self, data: list[dict[str, Any]]):
        values = [
            (row["url"], row["company_name"], json.dumps(row))
            for row in data
        ]
        return self.__db.execute_insert_many(UPSERT_DATA_IN_BATCH, values)

    # def upsert_companies(self, data: list[CompanyInfo]):
    #     values = [
    #         (row.url, row.company_name)
    #         for row in data
    #     ]
    #     return self.__db.execute_insert_many(UPSERT_COMPANIES_IN_BATCH, values)
