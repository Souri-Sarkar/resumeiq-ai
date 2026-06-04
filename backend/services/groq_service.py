from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_resume_feedback(resume_text, job_description):

    prompt = f"""
    You are an ATS recruiter.

    Resume:
    {resume_text[:3000]}

    Job Description:
    {job_description}

    Provide:
    1. Strengths
    2. Weaknesses
    3. Missing Skills
    4. ATS Suggestions

    Keep it concise.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content