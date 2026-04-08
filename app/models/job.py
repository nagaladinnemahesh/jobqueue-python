from sqlalchemy import Column, String, Integer, DateTime, JSON
from datetime import datetime
from app.db.base import Base
import uuid

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default = lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    payload = Column(JSON)
    status = Column(String, default="PENDING")
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default = 3)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)

