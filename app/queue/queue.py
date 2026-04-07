from rq import Queue
from app.queue.redis import redis_conn

job_queue = Queue("jobs", connection=redis_conn)