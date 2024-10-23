from fastapi import FastAPI
from app.api import resume_routes

app = FastAPI()

# Include the resume processing routes
app.include_router(resume_routes.router)

# Root path to check if the API is running
@app.get("/")
def read_root():
    return {"message": "Resume Processing API is running"}
