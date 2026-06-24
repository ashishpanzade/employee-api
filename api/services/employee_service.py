from sqlalchemy.orm import Session

from api.models.employee import Employee
from api.repositories.employee_repository import EmployeeRepository
from api.schemas.employee import EmployeeIn


class EmployeeService:
    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)

    def get_all_employees(self) -> list[Employee]:
        return self.repository.get_all()

    def get_employee_by_id(self, employee_id: int) -> Employee | None:
        return self.repository.get_by_id(employee_id)

    def create_employee(self, payload: EmployeeIn) -> Employee:
        return self.repository.create(payload.model_dump())
