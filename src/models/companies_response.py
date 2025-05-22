from typing import Any

from pydantic import BaseModel


class CompanyProcessed(BaseModel):
    url: str
    imported_data: dict[str, Any]
    processed_variables: dict[str, Any]
    imported_date: str
    last_processed_date: str


class CompaniesResponse(BaseModel):
    companies: list[CompanyProcessed]
