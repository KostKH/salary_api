from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str
    surname: str
    job_title: str
    is_active: bool | None
    is_superuser: bool | None

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class SalaryBase(BaseModel):
    salary: int
    employee_id: int
    next_increase_date: datetime


class SalaryCreate(SalaryBase):
    pass


class Salary(SalaryBase):
    id: int

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ErrorNotFound(BaseModel):
    message: str = 'Запрошенные данные не найдены'
