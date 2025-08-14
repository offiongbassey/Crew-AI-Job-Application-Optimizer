from crewai import Agent
from tools import docs_tool, file_tool, web_rag_tool, search_tool, scrape_tool, semantic_search_resume
import os
from verify import verify_link

serper_api_key = os.getenv("SEPER_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL")

multi_job_researcher = Agent(
    role="Job Hunter AI",
    goal=(
        "Find and summarize high-quality recent {location} {title} jobs for someone with {years} years of experience."
        " Use Google search to find job listings from LinkedIn, Indeed and RemoteRocketship."
        " Scrape each job page, extract the relevant data, and return a clean JSON array of 12 jobs."
    ),
    backstory=(
        "You're a highly skilled AI trained to search the web for fresh tech jobs and summarize them."
        " You aim to give job seekers an edge by finding great roles they may have missed."
    ),
    tools=[search_tool, scrape_tool],
    verbose=True,
    allow_delegation=False,
    model=openai_model,
)

single_job_researcher = Agent(
    role="Tech Job Researcher",
    goal="""
        Make sure to do amazing analysis on
        job posting to help job applicants
    """,
    backstory="""
        As a Job Researcher, your prowess in
        navigating and extracting critical
        information from job postings is unmatched.
        Your skills help pinpoint the necessary
        qualifications and skills sought
        by employers, forming the foundation for
        effective application tailoring.
    """,
    tools=[scrape_tool, search_tool],
    verbose=True,
    model=openai_model
)

profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="""
        Do incredible research on job applicants
        to help them stand out in the job market"
    """,
    backstory="""
        Equipped with analytical prowess, you dissect
        and synthesize information
        from diverse sources to craft comprehensive
        personal and professional profiles, laying the
        groundwork for personalized resume enhancements.
    """,
    tools=[scrape_tool, search_tool, semantic_search_resume],
    verbose=True,
    model=openai_model
)

resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="""
        Find all the best ways to make a
         "resume stand out in the job market.
    """,
    backstory="""
        With a strategic mind and an eye for detail, you
        excel at refining resumes to highlight the most
        relevant skills and experiences, ensuring they
        resonate perfectly with the job's requirements.
    """,
    tools=[scrape_tool, search_tool, semantic_search_resume],
    verbose=True,
    model=openai_model
)

message_writer = Agent(
    role="Outreach Message Writer",
    goal="Write effective LinkedIn messages and cold emails based on the resume and job requirements",
    backstory="""
        A persuasive tech-savvy communicator who crafts personalized, high-converting outreach messages 
        to help job seekers stand out and connect with recruiters.
    """,
    tools=[scrape_tool, search_tool, semantic_search_resume],
    verbose=True,
    model=openai_model
)

interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="""
        Create interview questions and talking points
         "based on the resume and job requirements
    """,
    backstory="""
        Your role is crucial in anticipating the dynamics of
        interviews. With your ability to formulate key questions
        and talking points, you prepare candidates for success,
        ensuring they can confidently address all aspects of the
        job they are applying for.
    """,
    tools=[scrape_tool, search_tool, semantic_search_resume],
    model=openai_model
)
