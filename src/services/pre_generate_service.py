from datetime import datetime
from typing import Any, Optional, List


class PreGenerateService:

    def generate(self, data: List[dict[str, Any]]) -> List[dict[str, Any]]:
        for company in data:
            self.__set_pre_defined_features(company)
        return data

    def __set_pre_defined_features(self, company: dict[str, Any]) -> None:
        founded_year = self.__parse_founded_year(company.get("founded_year"))
        company["company_age"] = self.__calculate_company_age(founded_year) if founded_year is not None else None
        company["usa_based_feature"] = self.__check_usa_based(company.get("headquarters_city"))

    @staticmethod
    def __parse_founded_year(value: Any) -> Optional[int]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def __calculate_company_age(founded_year: int) -> int:
        current_year = datetime.now().year
        return current_year - founded_year

    @staticmethod
    def __check_usa_based(headquarters_city: Any) -> bool:
        if isinstance(headquarters_city, str):
            return "usa" in headquarters_city.lower()
        return False
