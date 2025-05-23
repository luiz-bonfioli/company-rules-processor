from typing import Optional, List

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from starlette.requests import Request

from src.core.context import get_company_service
from src.core.database.logger import get_logger
from src.models.companies_response import CompaniesResponse
from src.models.import_response import ImportSummary
from src.models.rules import Rule

router = APIRouter(prefix='/v1/company', tags=['Company'])
logger = get_logger(__name__)

@router.post('/import-company-data', response_model=ImportSummary)
async def import_company_data(
        request: Request,
        file: Optional[UploadFile] = File(None),
        company_service=Depends(get_company_service)):
    """
    Endpoint to import company data from an uploaded CSV file or json data.

    Args:
        request (Request): The incoming HTTP request with json data.
        file (Optional[UploadFile]): The uploaded CSV file containing company data.
        company_service: Dependency-injected service for handling company-related logic.

    Returns:
        ImportSummary: A summary of the import operation.
    """
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        logger.debug("Processing JSON import data")
        data = await request.json()
        response = company_service.import_data(data)
        return response

    elif "multipart/form-data" in content_type:
        logger.debug("Processing multipart/form-data import")
        file = __validate_file(file)
        response = await company_service.import_file(file)
        return response

    else:
        logger.error(f"Unsupported Media Type: {content_type}")
        raise HTTPException(status_code=415, detail="Unsupported Media Type")


@router.post('/process-company')
async def process_company(urls: List[str], rules: List[Rule], company_service=Depends(get_company_service)):
    """
    Endpoint to process company data based on provided URLs and rules.

    Args:
        urls (List[str]): A list of URLs to process.
        rules (List[Rule]): A list of rules to apply during processing.
        company_service: Dependency-injected service for handling company-related logic.

    Returns:
        response: The result of the company processing operation.
    """
    logger.info(f"Processing companies")
    return company_service.process_company(urls, rules)


@router.get('/get-companies', response_model=CompaniesResponse)
async def get_companies(company_service=Depends(get_company_service)):
    """
    Endpoint to retrieve a list of previously processed companies.

    Args:
        company_service: Dependency-injected service for handling company-related logic.

    Returns:
        CompaniesResponse: A response containing the list of processed companies.
    """
    logger.info("Fetching previously processed companies")
    return company_service.get_companies_previously_processed()


def __validate_file(file: Optional[UploadFile]) -> UploadFile:
    """Ensure file is provided for multipart/form-data requests."""
    if not file:
        logger.error("File upload attempted without file present")
        raise HTTPException(status_code=400, detail="File is required for multipart upload")
    return file
