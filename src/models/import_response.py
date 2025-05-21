from pydantic import BaseModel


class ImportSummary(BaseModel):
    job_id: str
    rows_inserted: int
    rows_read: int
