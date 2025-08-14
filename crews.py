import time
import uuid
import json
from dotenv import load_dotenv
load_dotenv()
from crewai import Crew
from agents import multi_job_researcher, single_job_researcher, resume_strategist, profiler, message_writer, interview_preparer
from tasks import multi_job_search_task, single_job_search_task, resume_strategy_task, profile_task, message_writing_task, interview_preparation_task
from litellm import RateLimitError
from tools import read_pdf
import re

multi_job_search_crew = Crew(
    agents=[multi_job_researcher],
    tasks=[multi_job_search_task],
    verbose=True,
    planning=True
)

resume_optimization_crew = Crew(
    agents=[single_job_researcher, profiler, resume_strategist, message_writer, interview_preparer],
    tasks=[single_job_search_task, profile_task, resume_strategy_task, message_writing_task, interview_preparation_task],
    verbose=True,
    planning=True,
)

async def job_search_crew(job_title: str, years: str, location: str):
    inputs = {
        "title": job_title,
        "years": years,
        "location": location
    }

    for attempts in range(3):
        try:
            result = multi_job_search_crew.kickoff(inputs=inputs)
            print("result: ", result)
            job_list = json.loads(result.raw)

            return { "status": "success", "result": job_list}

        except RateLimitError:
            if attempts < 2:
                time.sleep(20)
            else:
                return {"error": "Rate limit exceeded"}
        except Exception as e:
            return {"error": str(e)}
        
async def job_preparation_crew(job_posting_url: str, file_path: str):
    inputs = {
        "job_posting_url": job_posting_url,
        "resume": read_pdf(file_path)
    }

    for attempts in range(3):
        try:
            result = resume_optimization_crew.kickoff(inputs=inputs)
            print("REsult: ", result)
            if isinstance(result.raw, dict):
                return {"status": "success", "result": result.raw}
            else:
                try:
                    clean_raw = re.sub(r"^```(?:json)?\n|\n```$", "", result.raw.strip())
                    json_result = json.loads(clean_raw)
                    return {"status": "success", "result": json_result}
                except Exception as e:
                    return {"error": f"Failed to parse response: {str(e)}"}


        except RateLimitError:
            if attempts < 2:
                time.sleep(20)
            else:
                return { "error": "Rate limit exceeded" }
        except Exception as e:
            return { "error": str(e) }

