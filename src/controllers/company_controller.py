from typing import Optional

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from starlette.requests import Request

from src.core.context import get_company_service
from src.models.import_response import ImportSummary

router = APIRouter(prefix='/v1/company', tags=['Company'])


@router.post('/import-company-data', response_model=ImportSummary)
async def import_company_data(
        request: Request,
        file: Optional[UploadFile] = File(None),
        rules_processor_service=Depends(get_company_service)
):
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        data = await request.json()
        response = rules_processor_service.process_data(data)
        return response

    elif "multipart/form-data" in content_type:
        file = validate_file(file)
        response = await rules_processor_service.process_file(file)
        return response

    else:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")


def validate_file(file: Optional[UploadFile]) -> UploadFile:
    """Ensure file is provided for multipart/form-data requests."""
    if not file:
        raise HTTPException(status_code=400, detail="File is required for multipart upload")
    return file
