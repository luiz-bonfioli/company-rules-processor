import uuid
from typing import Any

from fastapi import UploadFile

from src.commons.file_utils import parse_csv_to_dict
from src.models.import_response import ImportSummary
from src.repositories.company_repository import CompanyRepository


class CompanyService:

    def __init__(self, company_repository: CompanyRepository):
        self.__company_repository = company_repository

    async def import_file(self, file: UploadFile):
        data = await parse_csv_to_dict(file)
        return self.save_data(data)

    def import_data(self, data: list[dict[str, Any]]):
        return self.save_data(data)

    def save_data(self, data: list[dict[str, Any]]):
        job_id = str(uuid.uuid4())
        rows_inserted = self.__company_repository.insert_data(job_id, data)
        return ImportSummary(job_id=job_id, rows_inserted=rows_inserted, rows_read=len(data))
