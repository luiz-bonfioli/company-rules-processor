import json
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field, field_validator


class CompanyInfo(BaseModel):
    company_name: str
    url: str
    founded_year: int
    total_employees: int
    headquarters_city: str
    employee_locations: Dict[str, int]
    employee_growth_2Y: Optional[float] = Field(alias="employee_rowth_2Y")
    employee_growth_1Y: Optional[float]
    employee_growth_6M: Optional[float]
    description: Optional[str]
    industry: Optional[str]

    @field_validator("founded_year", "total_employees", mode="before")
    @classmethod
    def parse_ints(cls, v: Any) -> int:
        return int(v)

    @field_validator("employee_growth_2Y", "employee_growth_1Y", "employee_growth_6M", mode="before")
    @classmethod
    def parse_floats(cls, v: Any) -> Optional[float]:
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    @field_validator("employee_locations", mode="before")
    @classmethod
    def parse_json_dict(cls, v: Any) -> Dict[str, int]:
        if isinstance(v, str):
            return json.loads(v)
        return v
