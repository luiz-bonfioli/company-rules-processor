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
    """
    Service layer handling company data import, processing, and retrieval logic.
    It interacts with repositories and other services to perform business operations.
    """

    def __init__(self, company_repository: CompanyRepository):
        """
        Initialize with a CompanyRepository instance and instantiate dependent services.
        """
        self.__company_repository = company_repository
        self.__rules_processor_service = RulesProcessorService()
        self.__pre_generate_service = PreGenerateService()

    async def import_file(self, file: UploadFile):
        """
        Parses a CSV file asynchronously, pre-generates data,
        and saves it in the database.

        Args:
            file (UploadFile): CSV file uploaded by the client.

        Returns:
            ImportSummary: Summary of import operation (rows read and inserted).
        """
        data = await parse_csv_to_dict(file)
        pre_generated_data = self.__pre_generate_data(data)
        return self.__save_data(pre_generated_data)

    def import_data(self, data: list[dict[str, Any]]):
        """
        Takes already loaded data, pre-generates it, and saves it in the database.

        Args:
            data (list of dict): Raw company data.

        Returns:
            ImportSummary: Summary of import operation.
        """
        pre_generated_data = self.__pre_generate_data(data)
        return self.__save_data(pre_generated_data)

    def process_company(self, urls: List[str], rules: List[Rule]):
        """
        Processes company data based on given URLs and rules.
        Applies the rules to each company's imported data, saves processed data,
        and returns a list of processed results.

        Args:
            urls (List[str]): List of company URLs to process.
            rules (List[Rule]): List of rules to apply during processing.

        Returns:
            List[dict]: List of dictionaries with processed variables for each company.
        """
        processed_companies = []
        last_processed_date = datetime.now()
        for url in urls:
            company = self.__company_repository.fetch_by_url(url)
            if company:
                processed = self.__rules_processor_service.process_rules(company[2], rules)
                processed["company"] = company[1]
                processed_companies.append(processed)
                self.__save_processed_data(url, last_processed_date, processed)

        return processed_companies

    def get_companies_previously_processed(self) -> CompaniesResponse:
        """
        Retrieves companies that have been processed previously,
        maps raw database tuples to CompanyProcessed Pydantic models,
        and returns a CompaniesResponse model.

        Returns:
            CompaniesResponse: Contains a list of processed companies.
        """
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
        """
        Saves pre-generated data by upserting into the database.

        Args:
            data (list of dict): Pre-generated company data.

        Returns:
            ImportSummary: Summary of import operation.
        """
        rows_inserted = self.__company_repository.upsert_data(data)
        return ImportSummary(rows_inserted=rows_inserted, rows_read=len(data))

    def __pre_generate_data(self, data: list[dict[str, Any]]):
        """
        Calls the PreGenerateService to transform raw data before saving.

        Args:
            data (list of dict): Raw company data.

        Returns:
            list of dict: Transformed/pre-generated data.
        """
        return self.__pre_generate_service.generate(data)

    def __save_processed_data(self, url: str, last_processed_date: datetime, processed: dict[str, Any]):
        """
        Saves processed data and last processed timestamp for a company.

        Args:
            url (str): Company URL.
            last_processed_date (datetime): Timestamp of processing.
            processed (dict): Processed variables data.
        """
        self.__company_repository.upsert_processed_data(url, last_processed_date, processed)
