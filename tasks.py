from crewai import Task
from agents import multi_job_researcher, single_job_researcher, profiler, resume_strategist, message_writer, interview_preparer

multi_job_search_task = Task(
    description=(
        "1. Use your search tool to find recent {location} {title} jobs (last 7 days),"
        " posted on LinkedIn, Inddex and RemoteRocketship.\n"
        "2. Scrape the job listings to extract these details:\n"
        "- title, company, country, location, remote (true/false), years, tools (8–9), description (2 paragraphs), link.\n\n"
        "3. Return EXACTLY 12 job listings formatted as a JSON array. Do NOT include markdown or extra formatting.\n\n"
        "Each object must follow:\n"
        "{\n"
        "  'id': 'random UUID',\n"
        "  'title': '...',\n"
        "  'company': '...',\n"
        "  'country': '...',\n"
        "  'location': '...',\n"
        "  'remote': true or false,\n"
        "  'years': '...',\n"
        "  'tools': ['Python', 'SQL', ...],\n"
        "  'description': '...',\n"
        "  'link': 'direct job URL. Do not hallucinate or provide generate one.'\n"
        "}"
    ),
    expected_output="A valid, minified JSON array of 12 job objects. No markdown. No text before or after.",
    agent=multi_job_researcher,
)

single_job_search_task = Task(
    description=""""
        Analyze the job posting URL provided ({job_posting_url})
        to extract key skills, experiences, and qualifications
        required. Use the tools to gather content and identify
        and categorize the requirements.
    """,
    expected_output="""
        A structured list of job requirements, including necessary
        skills, qualifications, and experiences.
    """,
    agent=single_job_researcher,
    async_execution=True
)

profile_task = Task(
    description="""
        Given the raw resume content below, extract and structure the key profile information.

        Resume:
        {resume}

        Return the result as structured Markdown or dictionary with the following fields:
        - Full name
        - Email
        - Phone (if present)
        - Summary
        - Skills
        - Work experience
        - Education
    """,
    expected_output="""
        A structured Markdown or dictionary object with keys: name, email, phone, summary, skills,
        work experience, and education. No placeholder values. Only use what exists in the resume.
    """,
    agent=resume_strategist
)

resume_strategy_task = Task(
    description="""
        You are a resume strategist. Your job is to rewrite the candidate's resume using the original content
        and the job description provided.

        Resume:
        {resume}

        Make the rewritten resume closely align with the job description while:
        - Keeping the original name and contact details
        - Updating the summary and skills to highlight job-relevant strengths
        - Rephrasing experiences and projects to match the job context
        - Outputting a clean, ATS-friendly modern Markdown format

        Do not invent or add any information not in the resume.
    """,
    expected_output="""
        A tailored resume in Markdown format including name, contact, updated summary, skills, work experience,
        and education — all rewritten to fit the job description without adding fake information.
    """,
    context=[single_job_search_task, profile_task],
    agent=resume_strategist,
    output_file="./docs/tailored_resume-6.md"
)


message_writing_task = Task(
    description="Write LinkedIn message and cold email for the job.",
    expected_output=(
    "A JSON object with two fields:\n"
    "1. `linkedin_message`: A short, personalized LinkedIn message tailored to the job.\n"
    "2. `cold_email`: A professional cold email (2–3 short paragraphs) introducing yourself, expressing interest in the job, and highlighting relevant experience.\n\n"
    "Example format:\n"
    "{\n"
    "  \"linkedin_message\": \"Hi [Hiring Manager], I came across your job posting for [Job Title] and I’m very interested...\",\n"
    "  \"cold_email\": \"Subject: Application for [Job Title]\\n\\nDear [Hiring Manager], I hope this message finds you well...\"\n"
    "}"
    ),
    agent=message_writer,
    context=[single_job_search_task, profile_task],
    output_file="./docs/cold-message-6.md"
)

interview_preparation_task = Task(
    description="""
        Based on the tailored resume {resume} and the job requirements at {job_posting_url}, 
        generate personalized interview preparation materials.

        Include:
        - The full tailored resume in **Markdown** format. Use bold section titles (e.g. **Summary**, **Skills**, **Experience**, **Education**) and one line of space before and after each section.
        - A short personalized LinkedIn message.
        - A cold email outreach version.
        - 10 interview questions tailored to the resume and job.
        - Talking points (2–3) for each question to guide the candidate’s response.
        - A short paragraph summarizing how the resume aligns with the job post.

        Return a single JSON object.
        """,
            expected_output="""
        A valid JSON object with this structure:
        {
        "tailored_resume": "Markdown-formatted resume string with section titles bolded",
        "linkedin_message": "...",
        "cold_email": "...",
        "interview_questions": [
            {
            "question": "...",
            "talking_points": ["...", "..."]
            },
            ...
        ],
        "alignment_summary": "..."
        }
        """,
    output_file="./docs/interview_materials-6.md",
    context=[single_job_search_task,
        profile_task,
        resume_strategy_task,
        message_writing_task],
    agent=interview_preparer
)