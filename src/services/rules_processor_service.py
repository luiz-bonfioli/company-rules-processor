from typing import Any

from src.models.rules import Rule, Operation


class RulesProcessorService:

    def process_rules(self, company_data: dict[str, Any], rules: list[Rule]) -> dict[str, int]:
        results = {}
        for rule in rules:
            result = self.__evaluate_rule(company_data, rule)
            results[rule.feature_name] = result
        return results

    def __evaluate_rule(self, company_data: dict[str, Any], rule: Rule) -> int:
        input_value = company_data.get(rule.input)
        if input_value is None:
            return rule.default

        operation_type = rule.operation.get_type()
        condition = self.__evaluate_condition(operation_type, input_value, rule.operation)
        return rule.match if condition else rule.default

    @staticmethod
    def __evaluate_condition(operation_type: str, input_value: Any, operation: Operation) -> bool:
        if operation_type in ("greater_than", "less_than"):
            if not isinstance(input_value, (int, float)):
                return False

        if operation_type == "greater_than":
            return input_value > operation.greater_than
        elif operation_type == "less_than":
            return input_value < operation.less_than
        elif operation_type == "equal":
            return input_value == operation.equal
        else:
            raise ValueError(f"Unsupported operation: {operation_type}")
