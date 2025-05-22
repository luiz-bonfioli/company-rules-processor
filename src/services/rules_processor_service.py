from typing import Any

from src.models.rules import Rule, Operation


class RulesProcessorService:
    """
    Service responsible for applying a list of rules on company data
    and returning a dictionary of feature results based on those rules.
    """

    def process_rules(self, company_data: dict[str, Any], rules: list[Rule]) -> dict[str, int]:
        """
        Processes each rule against the provided company data and
        collects the results keyed by each rule's feature_name.

        Args:
            company_data (dict): A dictionary of company attributes.
            rules (list of Rule): List of rules to apply.

        Returns:
            dict: Mapping from feature_name to resulting int value from rule evaluation.
        """
        results = {}
        for rule in rules:
            result = self.__evaluate_rule(company_data, rule)
            results[rule.feature_name] = result
        return results

    def __evaluate_rule(self, company_data: dict[str, Any], rule: Rule) -> int:
        """
        Evaluates a single rule against the company data.

        - If the input value for the rule is missing, returns the rule's default.
        - Otherwise, evaluates the condition specified by the rule's operation.
        - Returns rule.match if the condition is True, else rule.default.

        Args:
            company_data (dict): Company data.
            rule (Rule): Rule to evaluate.

        Returns:
            int: Result of rule evaluation (match or default value).
        """
        input_value = company_data.get(rule.input)
        if input_value is None:
            return rule.default

        operation_type = rule.operation.get_type()
        condition = self.__evaluate_condition(operation_type, input_value, rule.operation)
        return rule.match if condition else rule.default

    @staticmethod
    def __evaluate_condition(operation_type: str, input_value: Any, operation: Operation) -> bool:
        """
        Evaluates the condition of a rule operation.

        - For 'greater_than' and 'less_than', ensures input_value is numeric.
        - Performs the comparison accordingly.
        - For 'equal', compares equality.

        Args:
            operation_type (str): Type of operation ("greater_than", "less_than", "equal").
            input_value (Any): Value from company data.
            operation (Operation): Operation details.

        Returns:
            bool: True if condition met, else False.

        Raises:
            ValueError: If the operation_type is unsupported.
        """
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
