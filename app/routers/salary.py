"""Роутеры для едпойнтов зарплаты."""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app import database, schemas
from app.crud.crud import salary_crud
from app.auth.authenticate import authenticate, check_superuser

router = APIRouter()


@router.get(
    path='/',
    summary='Посмотреть всю ведомость зарплат',
    response_model=list[schemas.Salary],
    dependencies=[Depends(check_superuser)])
async def get_all_salaries(
    session: database.AsyncSession = Depends(database.get_async_session),
) -> list[schemas.Salary]:
    return await salary_crud.get_all(session=session)

@router.post(
    path='/',
    summary='Назначить зарплату',
    response_model=schemas.Salary,
    dependencies=[Depends(check_superuser)])
async def create_salary(
    new_salary: schemas.SalaryCreate,
    session: database.AsyncSession = Depends(database.get_async_session),
) -> schemas.Salary:
    salary = await salary_crud.create(
        new_obj=new_salary,
        session=session)
    return salary

@router.get(
    path='/me',
    summary='Посмотреть свою зарплату',
    response_model=schemas.Salary,
    responses={404:{'model': schemas.ErrorNotFound}})
async def get_salary(
    session: database.AsyncSession = Depends(database.get_async_session),
    user_id: int = Depends(authenticate)
) -> schemas.Salary:
    salary = await salary_crud.get_by_field(
        required_field='employee_id',
        value=user_id,
        session=session)
    if not salary:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message':'Данные о зарплате не найдены.'})
    return salary