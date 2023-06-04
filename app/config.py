from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Salary API'
    database_url: str = 'sqlite+aiosqlite:///./salary.db'
    jwt_secret: str = 'SECRET_KEY'
    jwt_algorithm: str = 'HS256'
    jwt_effect_seconds: int = 86400

    class Config:
        env_file = '.env'


settings = Settings()