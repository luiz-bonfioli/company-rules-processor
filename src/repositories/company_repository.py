import json
import uuid
from typing import Any

from src.core.database.database import Database
from src.core.database.schema import INSERT_DATA_IN_BATCH, UPSERT_COMPANIES_IN_BATCH
from src.models.company_info import CompanyInfo


class CompanyRepository:

    def __init__(self, db: Database):
        self.__db = db

    def insert_data(self, job_id, data: list[dict[str, Any]]):
        values = [
            (str(uuid.uuid4()), job_id, json.dumps(row))
            for row in data
        ]
        return self.__db.execute_insert_many(INSERT_DATA_IN_BATCH, values)

    def upsert_companies(self, data: list[CompanyInfo]):
        values = [
            (row.url, row.company_name)
            for row in data
        ]
        return self.__db.execute_insert_many(UPSERT_COMPANIES_IN_BATCH, values)
