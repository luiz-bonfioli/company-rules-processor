from datetime import datetime
from typing import Any, Optional, List

# Keywords to detect if a company operates in SaaS or related domains
SAAS_KEYWORDS = {
    "saas", "software as a service", "big data", "business intelligence", "cloud management"
}


class PreGenerateService:
    """
    Service responsible for adding pre-defined features to company data
    before further processing, like calculating company age, detecting
    if company is USA-based, or if it is related to SaaS.
    """

    def generate(self, data: List[dict[str, Any]]) -> List[dict[str, Any]]:
        """
        Iterates over a list of companies and enriches each dictionary
        with pre-defined features.

        Args:
            data (List[dict]): List of company data dictionaries.

        Returns:
            List[dict]: The enriched list with added features.
        """
        for company in data:
            self.__set_pre_defined_features(company)
        return data

    def __set_pre_defined_features(self, company: dict[str, Any]) -> None:
        """
        Adds predefined features to a single company dictionary, including:
        - company_age (int or None)
        - is_usa_based (bool)
        - is_saas (bool)

        Args:
            company (dict): Company data dictionary to enrich.
        """
        founded_year = self.__parse_founded_year(company.get("founded_year"))
        company["company_age"] = self.__calculate_company_age(founded_year) if founded_year is not None else None
        company["is_usa_based"] = self.__check_usa_based(company.get("headquarters_city"))
        company["is_saas"] = self.__check_is_saas(company)

    @staticmethod
    def __parse_founded_year(value: Any) -> Optional[int]:
        """
        Attempts to convert the founded year value to an integer.

        Args:
            value (Any): The input value to parse.

        Returns:
            Optional[int]: Parsed year as int or None if invalid.
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def __calculate_company_age(founded_year: int) -> int:
        """
        Calculates the age of the company based on the current year.

        Args:
            founded_year (int): The year the company was founded.

        Returns:
            int: Age of the company in years.
        """
        current_year = datetime.now().year
        return current_year - founded_year

    @staticmethod
    def __check_usa_based(headquarters_city: Any) -> bool:
        """
        Checks if the company is based in the USA by looking for
        'usa' in the headquarters city string.

        Args:
            headquarters_city (Any): City string to check.

        Returns:
            bool: True if based in the USA, False otherwise.
        """
        if isinstance(headquarters_city, str):
            return "usa" in headquarters_city.lower()
        return False

    @staticmethod
    def __check_is_saas(company: dict[str, Any]) -> bool:
        """
        Determines if the company is related to SaaS or similar fields
        by checking certain text fields for keywords.

        Args:
            company (dict): Company data dictionary.

        Returns:
            bool: True if SaaS-related keywords found, False otherwise.
        """
        fields_to_check = [
            company.get("description", ""),
            company.get("industry", "")
        ]
        combined_text = " ".join(str(field or "").lower() for field in fields_to_check)
        return any(keyword in combined_text for keyword in SAAS_KEYWORDS)
