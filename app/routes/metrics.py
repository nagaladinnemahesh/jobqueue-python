from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.deps import get_db
from app.models.job import Job

metrics_router = APIRouter()

@metrics_router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):

    total_jobs = db.query(func.count(Job.id)).scalar()

    completed = db.query(func.count(Job.id)).filter(Job.status == "COMPLETED").scalar()

    failed = db.query(func.count(Job.id)).filter(Job.status == "FAILED").scalar()

    queued = db.query(func.count(Job.id)).filter(Job.status == "QUEUED").scalar()

    processing = db.query(func.count(Job.id)).filter(Job.status == "PROCESSING").scalar()

    return {
        "total_jobs": total_jobs,
        "completed": completed,
        "failed": failed,
        "queued": queued,
        "processing": processing
    }

