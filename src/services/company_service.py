from datetime import datetime
from typing import Any, List

from fastapi import UploadFile

from src.commons.file_utils import parse_csv_to_dict
from src.models.companies_response import CompaniesResponse, CompanyProcessed
from src.models.import_response import ImportSummary
from src.models.rules import Rule
from src.repositories.company_repository import CompanyRepository
from src.services.pre_generate_service import PreGenerateService
from src.services.rules_processor_service import RulesProcessorService


class CompanyService:

    def __init__(self, company_repository: CompanyRepository):
        self.__company_repository = company_repository
        self.__rules_processor_service = RulesProcessorService()
        self.__pre_generate_service = PreGenerateService()

    async def import_file(self, file: UploadFile):
        data = await parse_csv_to_dict(file)
        pre_generated_data = self.__pre_generate_data(data)
        return self.__save_data(pre_generated_data)

    def import_data(self, data: list[dict[str, Any]]):
        pre_generated_data = self.__pre_generate_data(data)
        return self.__save_data(pre_generated_data)

    def process_company(self, urls: List[str], rules: List[Rule]):
        processed_companies = []
        last_processed_date = datetime.now()
        for url in urls:
            company = self.__company_repository.fetch_by_url(url)
            processed = self.__rules_processor_service.process_rules(company[2], rules)
            processed["company"] = company[1]
            processed_companies.append(processed)
            self.__save_processed_data(url, last_processed_date, processed)

        return processed_companies

    def get_companies_previously_processed(self) -> CompaniesResponse:
        companies_processed = self.__company_repository.get_companies_previously_processed()
        companies = []
        for processed in companies_processed:
            companies.append(CompanyProcessed(url=processed[0],
                                              imported_data=processed[2],
                                              processed_variables=processed[3],
                                              imported_date=str(processed[4]) if processed[4] is not None else None,
                                              last_processed_date=str(processed[5]) if processed[5] is not None else None))

        return CompaniesResponse(companies=companies)

    def __save_data(self, data: list[dict[str, Any]]):
        rows_inserted = self.__company_repository.upsert_data(data)
        return ImportSummary(rows_inserted=rows_inserted, rows_read=len(data))

    def __pre_generate_data(self, data: list[dict[str, Any]]):
        return self.__pre_generate_service.generate(data)

    def __save_processed_data(self, url: str, last_processed_date: datetime, processed: dict[str, Any]):
        self.__company_repository.upsert_processed_data(url, last_processed_date, processed)
