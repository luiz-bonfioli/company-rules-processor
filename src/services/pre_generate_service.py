from datetime import datetime
from typing import Any, Optional, List

SAAS_KEYWORDS = {
    "saas", "software as a service", "big data", "business intelligence", "cloud management"
}


class PreGenerateService:

    def generate(self, data: List[dict[str, Any]]) -> List[dict[str, Any]]:
        for company in data:
            self.__set_pre_defined_features(company)
        return data

    def __set_pre_defined_features(self, company: dict[str, Any]) -> None:
        founded_year = self.__parse_founded_year(company.get("founded_year"))
        company["company_age"] = self.__calculate_company_age(founded_year) if founded_year is not None else None
        company["is_usa_based"] = self.__check_usa_based(company.get("headquarters_city"))
        company["is_saas"] = self.__check_is_saas(company)

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

    @staticmethod
    def __check_is_saas(company: dict[str, Any]) -> bool:
        fields_to_check = [
            company.get("description", ""),
            company.get("industry", "")
        ]
        combined_text = " ".join(str(field or "").lower() for field in fields_to_check)
        return any(keyword in combined_text for keyword in SAAS_KEYWORDS)
