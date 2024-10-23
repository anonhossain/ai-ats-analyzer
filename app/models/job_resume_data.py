from pydantic import BaseModel

# Define the model for job description and action input
class JobResumeData(BaseModel):
    job_desc: str
    action: str
