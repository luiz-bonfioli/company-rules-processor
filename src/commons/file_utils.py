import csv
from io import StringIO
from typing import Any

from fastapi import UploadFile


async def parse_csv_to_dict(file: UploadFile) -> list[dict[str, Any]]:
    content = await file.read()
    text = content.decode('utf-8')
    f = StringIO(text)
    reader = csv.DictReader(f)
    return [row for row in reader]
