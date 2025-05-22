import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.services.company_service import CompanyService
from src.models.import_response import ImportSummary
from src.models.rules import Rule, Operation

mock_data = [
    {"url": "https://www.nexuswave.tech", "is_saas": False, "industry": "Software Development", "company_age": 6,
     "description": "Application development environment with seamless deployment across platforms, annual licensing and implementation services",
     "company_name": "NexusWave Systems", "founded_year": "2019", "is_usa_based": False, "total_employees": "52",
     "employee_rowth_2Y": "61.5", "headquarters_city": "Toronto (Canada)", "employee_growth_1Y": "26.7",
     "employee_growth_6M": "14.2",
     "employee_locations": "{\"USA\": 15, \"Canada\": 31, \"UK\": 3, \"India\": 2, \"Brazil\": 1}"},
    {"url": "https://www.quantumaicorp.ai", "is_saas": False, "industry": "Artificial Intelligence",
     "company_age": 4,
     "description": "AI hardware accelerators with proprietary algorithm optimization software, one-time purchase with maintenance contracts",
     "company_name": "QuantumAI Corp", "founded_year": "2021", "is_usa_based": True, "total_employees": "34",
     "employee_rowth_2Y": "78.3", "headquarters_city": "Seattle (USA)", "employee_growth_1Y": "43.7",
     "employee_growth_6M": "21.4",
     "employee_locations": "{\"USA\": 29, \"Canada\": 3, \"France\": 1, \"Japan\": 1}"}]


@pytest.mark.asyncio
@patch("src.services.company_service.parse_csv_to_dict", new_callable=AsyncMock)
async def test_import_file_should_return_summary(mock_parse_csv):
    mock_parse_csv.return_value = mock_data

    mock_repo = MagicMock()
    mock_repo.upsert_data.return_value = 2

    service = CompanyService(company_repository=mock_repo)
    service._CompanyService__pre_generate_service.generate = MagicMock(return_value=mock_data)

    file_mock = MagicMock()

    result = await service.import_file(file_mock)

    assert result == ImportSummary(rows_inserted=2, rows_read=2)
    mock_repo.upsert_data.assert_called_once_with(mock_data)


def test_import_data_should_return_summary():
    mock_repo = MagicMock()
    mock_repo.upsert_data.return_value = 2

    service = CompanyService(company_repository=mock_repo)
    service._CompanyService__pre_generate_service.generate = MagicMock(return_value=mock_data)

    result = service.import_data(mock_data)

    assert result == ImportSummary(rows_inserted=2, rows_read=2)
    mock_repo.upsert_data.assert_called_once_with(mock_data)


def test_process_company_should_process_rules_and_save():
    mock_urls = ["https://www.cloudlogiclabs.com"]
    mock_company = ('https://www.cloudlogiclabs.com', 'CloudLogic Labs',
                    {'company_age': 4, 'company_name': 'CloudLogic Labs',
                     'description': 'Project management platform with integrated resource allocation, subscription-based pricing with tiered plans',
                     'employee_growth_1Y': '38.6', 'employee_growth_6M': '19.8',
                     'employee_locations': '{"USA": 32, "Canada": 3, "UK": 2, "India": 1}', 'employee_rowth_2Y': '85.2',
                     'founded_year': '2021', 'headquarters_city': 'Boston (USA)', 'industry': 'Software',
                     'is_saas': False, 'is_usa_based': True, 'total_employees': '38',
                     'url': 'https://www.cloudlogiclabs.com'},
                    {'age_feature': 1, 'company': 'CloudLogic Labs', 'head_count_feature': 1, 'is_saas_feature': 0,
                     'usa_based_feature': 1}, datetime(2025, 5, 22, 8, 55, 43, 944135),
                    datetime(2025, 5, 22, 9, 13, 43))

    mock_repo = MagicMock()
    mock_repo.fetch_by_url.return_value = mock_company

    mock_rule_processor = MagicMock()
    mock_rule_processor.process_rules.return_value = {'age_feature': 1, 'company': 'CloudLogic Labs',
                                                      'head_count_feature': 1, 'is_saas_feature': 0,
                                                      'usa_based_feature': 1}

    service = CompanyService(company_repository=mock_repo)
    service._CompanyService__rules_processor_service = mock_rule_processor

    service._CompanyService__save_processed_data = MagicMock()

    rules = [Rule(input='total_employees', feature_name='head_count_feature',
                  operation=Operation(greater_than=80, less_than=None, equal=None), match=0, default=1),
             Rule(input='company_age', feature_name='age_feature',
                  operation=Operation(greater_than=None, less_than=10, equal=None), match=1, default=0),
             Rule(input='is_usa_based', feature_name='usa_based_feature',
                  operation=Operation(greater_than=None, less_than=None, equal=True), match=1, default=0),
             Rule(input='is_saas', feature_name='is_saas_feature',
                  operation=Operation(greater_than=None, less_than=None, equal=True), match=1, default=0)]

    result = service.process_company(mock_urls, rules)

    assert result == [{'age_feature': 1, 'company': 'CloudLogic Labs', 'head_count_feature': 1, 'is_saas_feature': 0,
                       'usa_based_feature': 1}]
    mock_repo.fetch_by_url.assert_called_once_with("https://www.cloudlogiclabs.com")
    mock_rule_processor.process_rules.assert_called_once()
    service._CompanyService__save_processed_data.assert_called_once()


def test_get_companies_previously_processed_should_return_response():
    imported_data = {'company_age': 5, 'company_name': 'DataSync Technologies',
                     'description': 'Enterprise data integration platform enabling real-time data synchronization across multiple systems, monthly subscription with volume-based pricing',
                     'employee_growth_1Y': '41.3', 'employee_growth_6M': '22.5',
                     'employee_locations': '{"USA": 36, "Canada": 4, "Germany": 1, "Singapore": 1}',
                     'employee_rowth_2Y': '92.7',
                     'founded_year': '2020', 'headquarters_city': 'San Francisco (USA)', 'industry': 'Data Integration',
                     'is_saas': False, 'is_usa_based': True, 'total_employees': '42',
                     'url': 'https://www.datasynctech.io'}
    processed_variables = {'age_feature': 1, 'company': 'DataSync Technologies', 'head_count_feature': 1,
                           'is_saas_feature': 0,
                           'usa_based_feature': 1}

    imported_date = datetime(2025, 5, 22, 8, 55, 43, )

    last_processed_date = datetime(2025, 5, 22, 9, 13, 43)
    mock_processed = [
        ('https://www.datasynctech.io', 'DataSync Technologies',
         imported_data,
         processed_variables,
         imported_date,
         last_processed_date)
    ]
    mock_repo = MagicMock()
    mock_repo.get_companies_previously_processed.return_value = mock_processed

    service = CompanyService(company_repository=mock_repo)

    result = service.get_companies_previously_processed()

    assert result.companies[0].url == "https://www.datasynctech.io"
    assert result.companies[0].imported_data == imported_data
    assert result.companies[0].processed_variables == processed_variables
    assert result.companies[0].imported_date == "2025-05-22 08:55:43"
    assert result.companies[0].last_processed_date == "2025-05-22 09:13:43"
