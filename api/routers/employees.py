from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.db.database import get_db
from api.schemas.employee import EmployeeIn, EmployeeOut
from api.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.get("", response_model=List[EmployeeOut], summary="List all employees")
def list_employees(service: EmployeeService = Depends(get_employee_service)):
    """
    Returns all employee records from the database.

    Pulls from the employees table which is seeded with 8 records on first startup.
    """
    return service.get_all_employees()


@router.get("/{employee_id}", response_model=EmployeeOut, summary="Get employee by ID")
def get_employee(employee_id: int, service: EmployeeService = Depends(get_employee_service)):
    """
    Fetch a single employee by their ID.

    Returns 404 if no employee found with that ID.
    """
    employee = service.get_employee_by_id(employee_id)
    if employee is None:
        raise HTTPException(
            status_code=404,
            detail=f"No employee found with id {employee_id}"
        )
    return employee


@router.post("", response_model=EmployeeOut, status_code=201, summary="Create a new employee")
def create_employee(payload: EmployeeIn, service: EmployeeService = Depends(get_employee_service)):
    """
    Create a new employee record.

    Returns the created employee with its assigned ID.
    """
    return service.create_employee(payload)
