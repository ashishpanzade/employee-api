from sqlalchemy import Column, Integer, String, Numeric, Date

from api.db.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    city = Column(String(100), nullable=False)
    joined_on = Column(Date, nullable=False)
