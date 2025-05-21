from typing import Any, List

from fastapi import UploadFile

from src.commons.file_utils import parse_csv_to_dict
from src.models.import_response import ImportSummary
from src.models.rules import Rule
from src.repositories.company_repository import CompanyRepository
from src.services.rules_processor_service import RulesProcessorService


class CompanyService:

    def __init__(self, company_repository: CompanyRepository):
        self.__company_repository = company_repository
        self.__rules_processor_service = RulesProcessorService()

    async def import_file(self, file: UploadFile):
        data = await parse_csv_to_dict(file)
        return self.__save_data(data)

    def import_data(self, data: list[dict[str, Any]]):
        return self.__save_data(data)

    def process_company(self, urls: List[str], rules: List[Rule]):
        for url in urls:
            company = self.__company_repository.fetch_by_url(url)
            self.__rules_processor_service.process_rules(company[2], rules)

    def __save_data(self, data: list[dict[str, Any]]):
        rows_inserted = self.__company_repository.upsert_data(data)
        return ImportSummary(rows_inserted=rows_inserted, rows_read=len(data))
