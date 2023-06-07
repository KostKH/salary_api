from datetime import datetime
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from api.auth.authenticate import authenticate, check_superuser
from api.auth.hash_password import HashPassword
from api.auth.jwt_handler import create_access_token
from api.database import Base, get_async_session
from api.models import Salary, User
from api.schemas import SalaryCreate, UserCreate
from main import app

BASE_DIR = Path('.').absolute()
APP_DIR = BASE_DIR
TEST_DB_PATH = APP_DIR / 'salary_db/test.db'
SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite:///{TEST_DB_PATH}'


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)


async def override_get_async_session():
    async with TestingSessionLocal() as session:
        await session.execute(text('PRAGMA foreign_keys = ON'))
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


password_handler = HashPassword()
password_hash = password_handler.create_hash('testpassword123')

superuser = User(
    id=1,
    username='User1',
    password=password_hash,
    name='Виктор',
    surname='Тестовый1',
    job_title='Работник',
    is_active=True,
    is_superuser=True,
)

active_user = User(
    id=2,
    username='User2',
    password=password_hash,
    name='Виктор',
    surname='Тестовый2',
    job_title='Работник',
    is_active=True,
    is_superuser=False,
)
inactive_user = User(
    id=3,
    username='User3',
    password=password_hash,
    name='Виктор',
    surname='Тестовый3',
    job_title='Работник',
    is_active=False,
    is_superuser=False,
)
salaries = [
    {
        'salary': 200000,
        'employee_id': 1,
        'next_increase_date': datetime(2023, 12, 1),
    },
    {
        'salary': 150000,
        'employee_id': 2,
        'next_increase_date': datetime(2023, 11, 1)
    },
]


async def create_user(userdata):
    async with TestingSessionLocal() as session:
        await session.execute(text('PRAGMA foreign_keys = ON'))
        user_schema = UserCreate(**userdata.__dict__)
        prepared_data = user_schema.dict()
        user = User(**prepared_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        token = create_access_token(user.id)
        return user, token


@pytest_asyncio.fixture
async def create_users():
    tempusers = {}
    tempusers['superuser'] = await create_user(superuser)
    tempusers['active_user'] = await create_user(active_user)
    tempusers['inactive_user'] = await create_user(inactive_user)
    return tempusers


@pytest_asyncio.fixture
async def salaries_in_db(create_users):
    async with TestingSessionLocal() as session:
        await session.execute(text('PRAGMA foreign_keys = ON'))
        created_salary = []
        for salarydata in salaries:
            salary_schema = SalaryCreate(**salarydata)
            prepared_data = salary_schema.dict()
            salary = Salary(**prepared_data)
            session.add(salary)
            await session.commit()
            await session.refresh(salary)
            created_salary.append(salary.__dict__.copy())
        return created_salary, create_users


def override_failed_auth():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=('Для получения доступа авторизуйтейсь '
                'и добавьте токен в запрос.'))


@pytest.fixture
def superuser_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[check_superuser] = lambda: True
    with TestClient(app) as client:
        yield client


@pytest.fixture
def active_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[authenticate] = lambda: active_user
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[authenticate] = override_failed_auth
    with TestClient(app) as client:
        yield client
