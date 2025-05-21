import json
import uuid
from typing import Any

from src.core.database.database import Database
from src.core.database.schema import INSERT_DATA_IN_BATCH


class CompanyRepository:

    def __init__(self, db: Database):
        self.__db = db

    def insert_data(self, job_id, data: list[dict[str, Any]]):
        values = [
            (str(uuid.uuid4()), job_id, json.dumps(row))
            for row in data
        ]
        return self.__db.execute_insert_many(INSERT_DATA_IN_BATCH, values)


    def insert_companies(self, job_id, data: list[dict[str, Any]]):
        values = [
            (str(uuid.uuid4()), job_id, json.dumps(row))
            for row in data
        ]
        return self.__db.execute_insert_many(INSERT_DATA_IN_BATCH, values)
