import json
from datetime import datetime
from typing import Any

from src.core.database.database import Database
from src.core.database.schema import UPSERT_DATA_IN_BATCH, SELECT_COMPANY_BY_URL, UPDATE_PROCESSED_DATA, \
    SELECT_PREVIOUSLY_PROCESSED


class CompanyRepository:
    """
    Repository responsible for CRUD operations related to company data
    in the database.
    """

    def __init__(self, db: Database):
        """
        Initializes the repository with a database instance.

        Args:
            db (Database): The database connection wrapper.
        """
        self.__db = db

    def upsert_data(self, data: list[dict[str, Any]]):
        """
        Inserts or updates company data in batch.

        Args:
            data (list of dict): List of dictionaries, each representing company data.

        Returns:
            int: Number of rows affected by the batch upsert operation.
        """
        values = [
            (row["url"],
             row["company_name"],
             json.dumps(row),
             None,
             datetime.now(),
             None)
            for row in data
        ]
        return self.__db.execute_insert_many(UPSERT_DATA_IN_BATCH, values)

    def upsert_processed_data(self, url: str, last_processed_date: datetime, processed: dict[str, Any]):
        """
        Updates the processed data and last processed date for a company identified by URL.

        Args:
            url (str): The unique URL of the company.
            last_processed_date (datetime): Timestamp of last processing.
            processed (dict): Processed variables stored as JSON.

        Returns:
            int: Number of rows affected by the update.
        """
        values = (json.dumps(processed),
                  last_processed_date,
                  url)
        return self.__db.execute(UPDATE_PROCESSED_DATA, values)

    def fetch_by_url(self, url: str):
        """
        Retrieves a single company record by its URL.

        Args:
            url (str): The unique URL of the company.

        Returns:
            dict or None: The company record if found, else None.
        """
        return self.__db.fetch_one(SELECT_COMPANY_BY_URL, (url,))

    def get_companies_previously_processed(self):
        """
        Retrieves all companies that have previously been processed.

        Returns:
            list of dict: List of company records.
        """
        return self.__db.fetch_all(SELECT_PREVIOUSLY_PROCESSED)

