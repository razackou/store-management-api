from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

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
