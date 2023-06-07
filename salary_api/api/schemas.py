from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """Базовая схема пользователя с общими атрибутами для всех схем
    пользователя"""

    username: str
    name: str
    surname: str
    job_title: str
    is_active: bool | None
    is_superuser: bool | None


class UserCreate(UserBase):
    """Схема, используемая при создании пользователя"""

    password: str


class User(UserBase):
    """Схема, используемая при возврате данных о пользователе из БД."""

    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class SalaryBase(BaseModel):
    """Базовая схема для записей о зарплате и дате её повышения
    с общими атрибутами для всех схем зарплаты."""

    salary: int
    employee_id: int
    next_increase_date: datetime


class SalaryCreate(SalaryBase):
    """Схема, используемая при создании записи о зарплате
    и дате её повышения."""

    pass


class Salary(SalaryBase):
    """Схема для получения записей о зарплате из БД."""
    id: int

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    """Схема для возвращения пользователю данных о выпущенном токене."""
    access_token: str
    token_type: str


class ErrorNotFound(BaseModel):
    """Схема для сообщения об остутсвии данных в БД."""

    message: str = 'Запрошенные данные не найдены'
