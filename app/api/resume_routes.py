from fastapi import APIRouter, File, UploadFile
from app.models.job_resume_data import JobResumeData
from app.core.resume_processor import process_resume_action

router = APIRouter()

# API to process the resume and job description
@router.post("/process-resume/")
async def process_resume(data: JobResumeData, resume_file: UploadFile = File(...)):
    return await process_resume_action(data, resume_file)
