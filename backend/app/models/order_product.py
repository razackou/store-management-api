from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


class OrderProduct(Base):
    __tablename__ = "order_product"

    order_id = Column(
        Integer, ForeignKey("order.id", ondelete="CASCADE"), primary_key=True
    )
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
