from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    unit_price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)

    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    category = relationship("Category")
