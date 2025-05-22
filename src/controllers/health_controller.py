from datetime import datetime

from fastapi import APIRouter
from psycopg2 import OperationalError
from starlette.responses import JSONResponse

from src.core.context import get_database

router = APIRouter(prefix='', tags=['Health and Status'])


@router.get('/health', summary="Health check")
async def health():
    """
    Basic health check endpoint.

    Returns:
        dict: A simple status message indicating the service is up.
    """
    return {"status": "ok"}


@router.get("/status", summary="Detailed status check")
async def status():
    """
    Performs a detailed status check including database connectivity.

    Returns:
        JSONResponse: A JSON response indicating the health of dependencies
                      and current timestamp. Returns 503 if the database is unreachable.
    """
    try:
        db = get_database()
        db.execute("SELECT 1")
    except OperationalError:
        return JSONResponse(content={"database": "unreachable"}, status_code=503)

    return JSONResponse(
        content={
            "status": "ok",
            "timestamp": datetime.now().__str__(),
            "dependencies": {
                "database": "ok"
            }
        }
    )
