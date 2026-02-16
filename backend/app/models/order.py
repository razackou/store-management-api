from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    order_date = Column(TIMESTAMP, server_default=func.now())
    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(50), nullable=False)

    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employee.id"))

    client = relationship("Client")
    employee = relationship("Employee")
    products = relationship("OrderProduct", cascade="all, delete")
