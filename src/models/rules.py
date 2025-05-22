from typing import Optional

from pydantic import BaseModel


class Operation(BaseModel):
    """
    Represents a conditional operation that can be one of:
    - greater_than: checks if a value is greater than a given integer
    - less_than: checks if a value is less than a given integer
    - equal: checks if a value equals a boolean
    Only one of these should be defined at a time.
    """
    greater_than: Optional[int] = None
    less_than: Optional[int] = None
    equal: Optional[bool] = None

    def get_type(self) -> str:
        """
        Determines which operation type is defined and returns its name.

        Returns:
            str: The operation type as a string.

        Raises:
            ValueError: If no operation is defined.
        """
        if self.greater_than is not None:
            return "greater_than"
        elif self.less_than is not None:
            return "less_than"
        elif self.equal is not None:
            return "equal"
        else:
            raise ValueError("No valid operation defined")


class Rule(BaseModel):
    """
    Defines a rule that applies an operation on a given input feature and
    specifies the match and default integer values.

    Attributes:
        input (str): The input value or expression to evaluate.
        feature_name (str): The name of the feature to which the rule applies.
        operation (Operation): The conditional operation to perform.
        match (int): The integer value to return if the rule condition matches.
        default (int): The integer value to return if the rule condition does not match.
    """
    input: str
    feature_name: str
    operation: Operation
    match: int
    default: int
