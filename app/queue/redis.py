import redis
import os

redis_conn = redis.Redis(
    host = os.getenv("REDIS_HOST", "localhost"),
    port = 6379,
    db=0
)