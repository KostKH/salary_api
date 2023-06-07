from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from .database import Base


class User(Base):
    username = mapped_column(String, nullable=False, unique=True)
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
        sqlite_on_conflict_unique='REPLACE')
    next_increase_date = mapped_column(DateTime, nullable=False)
    employee = relationship("User", back_populates='salary')
