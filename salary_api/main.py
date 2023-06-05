from fastapi import FastAPI

from app.config import settings
from app.routers.main_router import main_router

app = FastAPI(title=settings.app_title)
app.include_router(main_router)
