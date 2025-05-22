import pytest
from src.services.rules_processor_service import RulesProcessorService
from src.models.rules import Rule, Operation


@pytest.fixture
def service():
    return RulesProcessorService()


def test_process_rules_should_apply_all_rules(service):
    rules = [
        Rule(input='total_employees', feature_name='head_count_feature',
             operation=Operation(greater_than=80, less_than=None, equal=None), match=0, default=1),
        Rule(input='company_age', feature_name='age_feature',
             operation=Operation(greater_than=None, less_than=10, equal=None), match=1, default=0),
    ]

    company_data = {'company_age': 4, 'company_name': 'CloudLogic Labs',
                    'description': 'Project management platform with integrated resource allocation, subscription-based pricing with tiered plans',
                    'employee_growth_1Y': '38.6', 'employee_growth_6M': '19.8',
                    'employee_locations': '{"USA": 32, "Canada": 3, "UK": 2, "India": 1}', 'employee_rowth_2Y': '85.2',
                    'founded_year': '2021', 'headquarters_city': 'Boston (USA)', 'industry': 'Software',
                    'is_saas': False, 'is_usa_based': True, 'total_employees': '38',
                    'url': 'https://www.cloudlogiclabs.com'}

    result = service.process_rules(company_data, rules)

    assert result == {'age_feature': 1, 'head_count_feature': 1}


def test_evaluate_rule_should_return_default_when_input_missing(service):
    rule = Rule(input='total_employees', feature_name='head_count_feature',
                operation=Operation(greater_than=80, less_than=None, equal=None), match=1, default=0)
    result = service._RulesProcessorService__evaluate_rule({}, rule)
    assert result == 0


def test_evaluate_condition_greater_than(service):
    operation = Operation(greater_than=100)
    assert service._RulesProcessorService__evaluate_condition("greater_than", 200, operation)
    assert not service._RulesProcessorService__evaluate_condition("greater_than", 50, operation)


def test_evaluate_condition_less_than(service):
    operation = Operation(less_than=100)
    assert service._RulesProcessorService__evaluate_condition("less_than", 50, operation)
    assert not service._RulesProcessorService__evaluate_condition("less_than", 150, operation)


def test_evaluate_condition_equal(service):
    operation = Operation(equal=True)
    assert service._RulesProcessorService__evaluate_condition("equal", "True", operation)
    assert not service._RulesProcessorService__evaluate_condition("equal", "False", operation)


def test_evaluate_condition_unsupported_operation_should_raise(service):
    operation = Operation()
    with pytest.raises(ValueError):
        service._RulesProcessorService__evaluate_condition("unknown", 10, operation)
