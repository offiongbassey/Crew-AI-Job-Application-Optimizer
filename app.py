from fastapi import FastAPI, UploadFile, Form, File
from crews import job_search_crew, job_preparation_crew
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class job_request(BaseModel):
    job_title: str
    years: str
    location: str

@app.post("/api/v1/submit-job-request")
async def submit_job_request(data: job_request):
    crew_result = await job_search_crew(data.job_title, data.years, data.location)

    print("Crew Test Result: ", crew_result)
    
    return crew_result

@app.post("/api/v1/resume-optimization")
async def optimize_resume_request(
    job_posting_url: str = Form(...),
    file: UploadFile = File(...)
):
    file_location = f"./docs/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    crew_result = await job_preparation_crew(job_posting_url, file_location)

    print("Crew Test Result: ", crew_result)

    return crew_result

