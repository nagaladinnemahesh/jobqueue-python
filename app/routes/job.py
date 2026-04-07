from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.job import Job
from app.queue.queue import job_queue
from app.workers.job_worker import process_job

router = APIRouter()


# create jobs

@router.post("/jobs")
def create_job(data: dict, db: Session = Depends(get_db)):
    job = Job(
        type = data.get("type"),
        payload = data.get("payload"),
        status = "QUEUED"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    #push to queue
    job_queue.enqueue(process_job, job.id)

    return {
        "id":job.id,
        "status": job.status
    }


# get all jobs
@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()

    return [
        {
            "id": j.id,
            "type": j.type,
            "status": j.status,
        }
        for j in jobs
    ]


# get job by id

@router.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}
    
    return {
        "id": job.id,
        "type": job.type,
        "status": job.status
    }

