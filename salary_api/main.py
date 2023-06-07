from fastapi import FastAPI

from api.config import settings
from api.routers.main_router import main_router

app = FastAPI(title=settings.app_title)
app.include_router(main_router)
