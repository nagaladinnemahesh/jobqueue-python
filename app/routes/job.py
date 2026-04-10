from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.job import Job
from app.queue.queue import job_queue
from app.workers.job_worker import process_job
from app.schemas.job import JobCreate

router = APIRouter()


# create jobs

@router.post("/jobs")
def create_job(job_data: JobCreate, db: Session=Depends(get_db)):
    new_job = Job(
        type = job_data.type,
        payload = job_data.payload,
        status = "QUEUED"
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    #push to queue
    job_queue.enqueue(process_job, new_job.id)

    return {
        "id":new_job.id,
        "status": new_job.status
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

