from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.info import router as info_router
from app.core.config import settings
from app.db.database import engine
from app.db.base import Base
from app.models.job import Job

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
app.include_router(info_router)

Base.metadata.create_all(bind=engine)