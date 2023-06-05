from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    app_title: str = 'Salary API'
    database_url: str = os.getenv(
        'DATABASE_URL',
        'sqlite+aiosqlite:///salary_db/salary.db')
    jwt_secret: str = os.getenv('JWT_SECRET_KEY', 'some_key')
    jwt_algorithm: str = os.getenv('JWT_ALGORITHM', 'HS256')
    jwt_effect_seconds: int = int(os.getenv('JWT_EFFECT_SECONDS', 86400))

settings = Settings()