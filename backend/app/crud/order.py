from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_product import OrderProduct
from app.models.product import Product
from app.schemas.order import OrderCreate


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def create_order(db: Session, data: OrderCreate):
    total = Decimal("0.00")

    order = Order(
        client_id=data.client_id,
        employee_id=data.employee_id,
        status=data.status,
        total_amount=0,
    )
    db.add(order)
    db.flush()

    for item in data.products:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise ValueError(f"Product with id {item.product_id} not found")
        total += product.unit_price * item.quantity

        db.add(
            OrderProduct(
                order_id=order.id, product_id=item.product_id, quantity=item.quantity
            )
        )

    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if not order:
        return None
    db.delete(order)
    db.commit()
    return order
