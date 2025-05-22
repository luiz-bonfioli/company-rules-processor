import csv
from io import StringIO
from typing import Any

from fastapi import UploadFile


async def parse_csv_to_dict(file: UploadFile) -> list[dict[str, Any]]:
    """
    Asynchronously parses a CSV file into a list of dictionaries.

    Args:
        file (UploadFile): The uploaded CSV file.

    Returns:
        list[dict[str, Any]]: A list where each item is a dictionary representing a row in the CSV.
    """
    content = await file.read()
    text = content.decode('utf-8')
    f = StringIO(text)
    reader = csv.DictReader(f)
    return [row for row in reader]
