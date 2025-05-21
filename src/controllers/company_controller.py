from typing import Optional, List

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from starlette.requests import Request

from src.core.context import get_company_service
from src.models.import_response import ImportSummary
from src.models.rules import Rule

router = APIRouter(prefix='/v1/company', tags=['Company'])


@router.post('/import-company-data', response_model=ImportSummary)
async def import_company_data(
        request: Request,
        file: Optional[UploadFile] = File(None),
        company_service=Depends(get_company_service)
):
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        data = await request.json()
        response = company_service.import_data(data)
        return response

    elif "multipart/form-data" in content_type:
        file = __validate_file(file)
        response = await company_service.import_file(file)
        return response

    else:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")


@router.post('/process-company', response_model=str)
async def process_company(urls: List[str], rules: List[Rule], company_service=Depends(get_company_service)):
    company_service.process_company(urls, rules)
    return ""


def __validate_file(file: Optional[UploadFile]) -> UploadFile:
    """Ensure file is provided for multipart/form-data requests."""
    if not file:
        raise HTTPException(status_code=400, detail="File is required for multipart upload")
    return file
