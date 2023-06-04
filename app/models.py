from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.orm import mapped_column

class User(Base):
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    salary = relationship('Salary', back_populates='employee')


class Salary(Base):
    salary = Column(Integer, nullable=False)
    employee_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    next_increase_date = Column(DateTime, nullable=False)
    employee = relationship("User", back_populates='salary')
    __table_args__ = (
        UniqueConstraint(
            'employee_id', 
            name='uc_salary_employee_id',
            sqlite_on_conflict='REPLACE'),
    )


