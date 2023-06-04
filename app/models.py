from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.orm import mapped_column

class User(Base):
    username = mapped_column(String, nullable=False)
    password = mapped_column(String, nullable=False)
    name = mapped_column(String, nullable=False)
    surname = mapped_column(String, nullable=False)
    job_title = mapped_column(String, nullable=False)
    is_active = mapped_column(Boolean, default=True)
    is_superuser = mapped_column(Boolean, default=False)
    salary = relationship('Salary', back_populates='employee')


class Salary(Base):
    salary = mapped_column(Integer, nullable=False)
    employee_id = mapped_column(
        Integer,
        ForeignKey('user.id'),
        nullable=False,
        unique=True, 
        sqlite_on_conflict_unique='REPLACE'
    )
    next_increase_date = mapped_column(DateTime, nullable=False)
    employee = relationship("User", back_populates='salary')
    '''
    __table_args__ = (
        UniqueConstraint(
            'employee_id', 
            name='uc_salary_employee_id',
            sqlite_on_conflict='REPLACE'),
    )
    '''

