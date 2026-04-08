from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.models.job import Job
from app.queue.queue import job_queue
from app.workers.job_worker import process_job

def recover_stuck_jobs():
    db = SessionLocal()

    #define stuck threshold
    try:
        threshold_time = datetime.utcnow() - timedelta(seconds=30)

        jobs = db.query(job).filter(
            Job.status == "QUEUED",
            Job.created_at < threshold_time,
            Job.attempts < Job.max_attempts
        ).all()

        if not jobs:
            print("[RECOVERY] Not stuck jobs found")
            return

        for job in jobs:
            print(f"[RECOVERY] Re-enqueue job {job.id}")
            job_queue.enqueue(process_job, job.id)

    except Exception as e:
        print(f"[RECOVERY ERROR] {str(e)}")
    
    finally:
        db.close()