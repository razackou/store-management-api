from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.crud.employee import get_employee, get_employees, create_employee, update_employee, delete_employee

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=list[EmployeeRead])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_employees(db, skip, limit)

@router.get("/{employee_id}", response_model=EmployeeRead)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/", response_model=EmployeeRead)
def create_new_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, employee)

@router.put("/{employee_id}", response_model=EmployeeRead)
def update_existing_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    updated = update_employee(db, employee_id, employee)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@router.delete("/{employee_id}", response_model=EmployeeRead)
def delete_existing_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return deleted
