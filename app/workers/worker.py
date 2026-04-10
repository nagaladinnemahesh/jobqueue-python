from dotenv import load_dotenv
import os

import logging
import threading
import time
from rq import Worker, Queue

from app.queue.redis import redis_conn
from app.recovery.recover_jobs import recover_stuck_jobs

load_dotenv()
print("WORKER DB URL:", os.getenv("DATABASE_URL"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Background recovery thread
def recovery_loop(interval=30):
    while True:
        try:
            logger.info("[RECOVERY] Running recovery job...")
            recover_stuck_jobs()
        except Exception as e:
            logger.error(f"[RECOVERY ERROR] {str(e)}")

        time.sleep(interval)


if __name__ == "__main__":
    logger.info(" Worker starting...")

    # Start recovery in background thread
    recovery_thread = threading.Thread(
        target=recovery_loop,
        daemon=True
    )
    recovery_thread.start()

    logger.info("Worker listening on 'jobs' queue...")

    # Start RQ worker with scheduler
    worker = Worker([Queue("jobs", connection=redis_conn)])
    worker.work(with_scheduler=True)