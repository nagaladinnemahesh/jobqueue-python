from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.info import router as info_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
app.include_router(info_router)