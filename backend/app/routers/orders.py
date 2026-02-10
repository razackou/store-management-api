from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderRead
from app.crud.order import create_order, get_order, get_orders, delete_order

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=list[OrderRead])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_orders(db, skip, limit)

@router.get("/{order_id}", response_model=OrderRead)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderRead)
def create(data: OrderCreate, db: Session = Depends(get_db)):
    try:
        return create_order(db, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{order_id}", response_model=OrderRead)
def delete(order_id: int, db: Session = Depends(get_db)):
    deleted = delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted
