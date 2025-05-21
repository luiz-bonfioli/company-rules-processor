from pydantic import BaseModel


class ImportSummary(BaseModel):
    rows_inserted: int
    rows_read: int
