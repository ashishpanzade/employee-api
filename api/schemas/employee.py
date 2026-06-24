from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class EmployeeIn(BaseModel):
    name: str
    department: str
    role: str
    salary: Decimal
    city: str
    joined_on: date


class EmployeeOut(BaseModel):
    id: int
    name: str
    department: str
    role: str
    salary: Decimal
    city: str
    joined_on: date

    # Allows Pydantic to read attributes from SQLAlchemy ORM objects 
    model_config = {"from_attributes": True}
