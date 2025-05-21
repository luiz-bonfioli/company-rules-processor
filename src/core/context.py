from src.services.company_service import CompanyService


def get_company_service() -> CompanyService:
    return CompanyService()