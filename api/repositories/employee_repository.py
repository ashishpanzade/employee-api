from sqlalchemy.orm import Session

from api.models.employee import Employee


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Employee]:
        return self.db.query(Employee).all()

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def create(self, data: dict) -> Employee:
        employee = Employee(**data)
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee
