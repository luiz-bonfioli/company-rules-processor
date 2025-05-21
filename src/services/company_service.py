from typing import Any, List

from fastapi import UploadFile

from src.commons.file_utils import parse_csv_to_dict
from src.models.company_info import CompanyInfo
from src.models.import_response import ImportSummary
from src.models.rules import Rule
from src.repositories.company_repository import CompanyRepository


class CompanyService:

    def __init__(self, company_repository: CompanyRepository):
        self.__company_repository = company_repository

    async def import_file(self, file: UploadFile):
        data = await parse_csv_to_dict(file)
        # self.__save_companies(data)
        return self.__save_data(data)

    def import_data(self, data: list[dict[str, Any]]):
        return self.__save_data(data)

    def process_company(self, urls: List[str], rules: List[Rule]):
        # print(urls)
        # for rule in rules:
        #     print(rule)
        #     print(rule.operation.get_type())
        pass

    def __save_data(self, data: list[dict[str, Any]]):
        rows_inserted = self.__company_repository.upsert_data(data)
        return ImportSummary(rows_inserted=rows_inserted, rows_read=len(data))

    # def __save_companies(self, data):
    #     companies = [CompanyInfo(**company) for company in data]
    #     self.__company_repository.upsert_companies(companies)
