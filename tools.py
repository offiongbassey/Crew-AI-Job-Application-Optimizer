from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool,
    ScrapeWebsiteTool,
    PDFSearchTool
)
from crewai.tools import BaseTool
import fitz  # PyMuPDF

import requests
import uuid
from typing import ClassVar, Optional
from pydantic import BaseModel, Field
import os

docs_tool = DirectoryReadTool(directory="./job-posts")
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

semantic_search_resume = PDFSearchTool(pdf_path='./docs/fake_resume.pdf')


class FixedSerperTool(SerperDevTool):
    def run(self, search_query: str, **kwargs):
        return super().run(search_query=search_query, **kwargs)
    
search_tool = FixedSerperTool()
scrape_tool = ScrapeWebsiteTool()




class PDFReaderTool:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        doc = fitz.open(self.file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
def read_pdf(file_path):
    resume_text = PDFReaderTool(file_path).read()
    return resume_text
    
# class RemoteOKToolSchema(BaseModel):
#     search_query: str = Field(..., description="Keyword to filter jobs (e.g., 'data science')")


# class RemoteOKTool(BaseTool):
#     name: ClassVar[str]=  "RemoteOK Job Fetcher"
#     description: str = "Fetch remote jobs from RemoteOK API based on a search keyword."
#     args_schema = RemoteOKToolSchema  # ✅ Don't wrap in ClassVar

#     def _run(self, search_query: str) -> list:
#         url = "https://remoteok.io/api"
#         resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         jobs = resp.json()[1:]  # Skip metadata row

#         filtered_jobs = []
#         for job in jobs:
#             title = job.get("position", "")
#             description = job.get("description", "")

#             if search_query.lower() not in (title + " " + description).lower():
#                 continue

#             filtered_jobs.append({
#                 "id": str(uuid.uuid4()),
#                 "title": title,
#                 "company": job.get("company", ""),
#                 "country": job.get("location", "Remote"),
#                 "location": job.get("location", "Remote"),
#                 "remote": True,
#                 "tools": job.get("tags", [])[:9],
#                 "description": description.replace("\n", " "),
#                 "link": job.get("url", "")
#             })

#         return filtered_jobs[:10]
    
# class IndeedToolSchema(BaseModel):
#     search_query: str = Field(..., description="Keyword to search Indeed jobs (e.g., 'data science')")
#     location: Optional[str] = Field(None, description="Job location filter (optional)")

# class IndeedTool(BaseTool):
#     name: ClassVar[str] = "Indeed Job Fetcher"
#     description: str = "Fetch jobs from Indeed via SerpAPI based on a search keyword."
#     args_schema = IndeedToolSchema

#     def _run(self, search_query: str, location: Optional[str] = None) -> list:
#         api_key = os.getenv("SERPER_API_KEY")
#         if not api_key:
#             raise ValueError("Missing SERPER_API_KEY in environment variables")

#         params = {
#             "engine": "indeed",
#             "q": search_query,
#             "l": location or "worldwide",
#             "api_key": api_key
#         }
#         if location:
#             params["location"] = location

#         resp = requests.get("https://serpapi.com/search", params=params)
#         data = resp.json()

#         jobs = []
#         for job in data.get("jobs_results", []):
#             jobs.append({
#                 "id": str(uuid.uuid4()),
#                 "title": job.get("title", ""),
#                 "company": job.get("company_name", ""),
#                 "country": job.get("location", ""),
#                 "location": job.get("location", ""),
#                 "remote": "remote" in job.get("location", "").lower(),
#                 "tools": [],  # SerpAPI doesn't provide tags
#                 "description": job.get("description", "").replace("\n", " "),
#                 "link": job.get("related_links", [{}])[0].get("link", ""),
#             })

#         return jobs[:10]




