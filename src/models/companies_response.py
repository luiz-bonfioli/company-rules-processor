from typing import Any

from pydantic import BaseModel


class CompanyProcessed(BaseModel):
    """
    Represents a company that has been processed, including
    its data, processing metadata, and timestamps.

    Attributes:
        url (str): The URL associated with the company.
        imported_data (dict[str, Any]): The raw data imported for the company.
        processed_variables (dict[str, Any]): Variables derived from processing the imported data.
        imported_date (str): The date when the data was imported (ISO format string).
        last_processed_date (str): The date when the company data was last processed (ISO format string).
    """
    url: str
    imported_data: dict[str, Any]
    processed_variables: dict[str, Any]
    imported_date: str
    last_processed_date: str


class CompaniesResponse(BaseModel):
    """
    Response model containing a list of processed companies.

    Attributes:
        companies (list[CompanyProcessed]): List of processed companies.
    """
    companies: list[CompanyProcessed]
