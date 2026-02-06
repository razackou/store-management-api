from sqlalchemy import Column, Integer, String
from app.database import Base

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    position = Column(String(100))
