from typing import Any

from fastapi import UploadFile

from src.commons.file_utils import parse_csv_to_dict
from src.models.import_response import ImportSummary


class CompanyService:

    async def process_file(self, file: UploadFile):
        data = await parse_csv_to_dict(file)
        return self.save_data(data)

    def process_data(self, data: list[dict[str, Any]]):
        return self.save_data(data)

    @staticmethod
    def save_data(data: list[dict[str, Any]]):
        print(data)
        return ImportSummary(rows_inserted=0, rows_read=0)
