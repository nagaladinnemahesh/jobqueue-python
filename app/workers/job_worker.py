from app.db.database import SessionLocal
from app.models.job import Job
import time
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def process_job(job_id: str):
    db = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        logger.error(f"[JOB NOT FOUND]{job_id}")
        return
    
    try:
        #mark processing
        job.status = "PROCESSING"
        job.attempts += 1
        db.commit()

        # print(f"Processing job {job_id}, attempt {job.attempts}")
        logger.info(f"[START] Job {job.id} | Attempt {job.attempts}")

        #stimulate work
        import random
        if random.random() < 0.5:
            raise Exception("Random failure")
        
        #success
        job.status = "COMPLETED"
        db.commit()

        logger.info(f"[SUCCESS] Job {job.id}")

    except Exception as e:
        logger.error(f"[FAILED] Job {job.id} | Attempt {job.attempts} | Error: {str(e)}")

        if job.attempts >= job.max_attempts:
            job.status = "FAILED"
            db.commit()
            logger.error(f"[FAILED] Job {job.id} | Attempt {job.attempts} | Error: {str(e)}")
        else:
            job.status = "QUEUED"

            #exponential
            delay = min(2 ** job.attempts,30)
            from app.queue.queue import job_queue
            job_queue.enqueue_in(timedelta(seconds=delay),process_job, job_id)

            logger.info(f"[RETRY] Job {job.id} in {delay}s")
        
        db.commit()
    
    finally:
        db.close()