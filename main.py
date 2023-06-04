from fastapi import FastAPI

from app.routers.main_router import main_router
from app.config import settings

app = FastAPI(title=settings.app_title)
app.include_router(main_router)