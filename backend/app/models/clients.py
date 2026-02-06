from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(30))
    address = Column(Text)