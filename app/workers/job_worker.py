from app.db.database import SessionLocal
from app.models.job import Job
import time
from datetime import timedelta
import logging
from app.services.email_service import send_email

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def process_job(job_id: str):
    db = SessionLocal()

    try:
        # acquire lock
        rows_updated = db.query(Job).filter(
            Job.id == job_id,
            Job.status == "QUEUED"
        ).update({"status":"PROCESSING"})

        if rows_updated == 0:
            print(f"[SKIP] Job {job_id} already taken")
            return
        
        db.commit() #commit lock

        #fetch job

        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            logger.error(f"[JOB NOT FOUND]{job_id}")
            return

        # process
        job.attempts += 1
        db.commit()

        # print(f"Processing job {job_id}, attempt {job.attempts}")
        logger.info(f"[START] Job {job.id} | Attempt {job.attempts}")

        #execution logic

        logger.info(f"[DEBUG] Job type: {job.type}")
        job_type = job.type.lower().replace("-", "_")
        if job_type == "send_email":
            from app.services.email_service import send_email
            send_email(job.payload)
        else:
            raise Exception(f"Unknow job type: {job_type}")

        #stimulate work
        # import random
        # if random.random() < 0.5:
        #     raise Exception("Random failure")
        
        #success
        job.status = "COMPLETED"
        db.commit()

        logger.info(f"[SUCCESS] Job {job.id}")

    except Exception as e:
        db.rollback()
        logger.error(f"[FAILED] Job {job.id} | Error: {str(e)}")

        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            return

        if job.attempts >= job.max_attempts:
            job.status = "FAILED"
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