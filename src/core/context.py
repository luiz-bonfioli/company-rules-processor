from src.commons.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from src.core.database.database import Database
from src.repositories.company_repository import CompanyRepository
from src.services.company_service import CompanyService


def get_database():
    db = Database()
    db.connect(host=DB_HOST,
               port=DB_PORT,
               dbname=DB_NAME,
               user=DB_USER,
               password=DB_PASSWORD)
    return db


def get_company_service() -> CompanyService:
    return CompanyService(company_repository=get_company_repository())


def get_company_repository():
    return CompanyRepository(db=get_database())
