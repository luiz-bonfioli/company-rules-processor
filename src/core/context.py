from src.commons.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from src.core.database.database import Database
from src.repositories.company_repository import CompanyRepository
from src.services.company_service import CompanyService


def get_database():
    """
    Creates and returns a connected Database instance
    using configuration parameters for the connection.

    Returns:
        Database: A connected Database object.
    """
    db = Database()
    db.connect(host=DB_HOST,
               port=DB_PORT,
               dbname=DB_NAME,
               user=DB_USER,
               password=DB_PASSWORD)
    return db


def get_company_service() -> CompanyService:
    """
    Creates and returns an instance of CompanyService,
    injecting the CompanyRepository dependency.

    Returns:
        CompanyService: Service object to handle company-related business logic.
    """
    return CompanyService(company_repository=get_company_repository())


def get_company_repository():
    """
    Creates and returns a CompanyRepository instance,
    injecting a connected Database instance.

    Returns:
        CompanyRepository: Repository object to handle database operations for companies.
    """
    return CompanyRepository(db=get_database())
