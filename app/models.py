from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    username = Column(String)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    job_title = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    salary = relationship('Salary', back_populates='employee')


class Salary(Base):
    salary = Column(Integer)
    employee_id = Column(Integer, ForeignKey('user.id'))
    next_increase_date = Column(DateTime)
    employee = relationship("User", back_populates='salary')
    __table_args__ = (
        UniqueConstraint('employee_id', 'id', name='_emloyee_salary_uc'),
    )


