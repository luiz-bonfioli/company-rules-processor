from typing import Optional

from pydantic import BaseModel


class Operation(BaseModel):
    greater_than: Optional[int] = None
    less_than: Optional[int] = None
    equal: Optional[bool] = None

    def get_type(self) -> str:
        if self.greater_than is not None:
            return "greater_than"
        elif self.less_than is not None:
            return "less_than"
        elif self.equal is not None:
            return "equal"
        else:
            raise ValueError("No valid operation defined")


class Rule(BaseModel):
    input: str
    feature_name: str
    operation: Operation
    match: int
    default: int
