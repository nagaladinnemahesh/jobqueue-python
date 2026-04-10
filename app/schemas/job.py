from pydantic import BaseModel, Field

class JobCreate(BaseModel):
    type: str = Field(..., description="Type of job (e.g., send_email)", example="send_email")
    payload: dict = Field(..., description="Data required for the job", example={
            "to": "your_email@gmail.com",
            "subject": "Test Email",
            "body": "Hello from async system"
        })

    class Config:
        schema_extra = {
            "example": {
                "type": "send_email",
                "payload": {
                    "to": "your_email@gmail.com",
                    "subject": "Test Email",
                    "body": "Hello from async system"
                }
            }
        }