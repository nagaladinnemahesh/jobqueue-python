from app.db.database import SessionLocal
from app.models.job import Job
import time

def process_job(job_id: str):
    db = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        print("Job not found")
        return
    
    print(f"Processing job {job_id}")

    #stimulate work
    time.sleep(3)

    job.status = "COMPLETED"
    db.commit()

    db.close()