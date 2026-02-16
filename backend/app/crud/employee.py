from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee_data: EmployeeCreate):
    employee = Employee(**employee_data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, employee_data: EmployeeUpdate):
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    for key, value in employee_data.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    db.delete(employee)
    db.commit()
    return employee
