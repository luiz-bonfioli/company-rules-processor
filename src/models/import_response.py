from pydantic import BaseModel


class ImportSummary(BaseModel):
    """
    Represents a summary of an import operation.

    Attributes:
        rows_inserted (int): The number of rows successfully inserted into the database.
        rows_read (int): The total number of rows read from the source file.
    """
    rows_inserted: int
    rows_read: int
