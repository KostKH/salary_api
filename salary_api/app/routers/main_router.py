"""Подключение всех роутеров к главному роутеру.
"""
from fastapi import APIRouter

from . import salary, user

main_router = APIRouter(prefix='/v1')

main_router.include_router(
    router=salary.router,
    prefix='/salary',
    tags=['Salary'],
)
main_router.include_router(
    router=user.router,
    prefix='/user',
    tags=['Users']
)
