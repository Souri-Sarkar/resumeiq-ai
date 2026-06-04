from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_resume_feedback(resume_text, job_description):

    prompt = f"""
    You are an expert ATS recruiter.

    Resume:
    {resume_text[:3000]}

    Job Description:
    {job_description}

    Give:
    1. Resume Strengths
    2. Resume Weaknesses
    3. Missing Skills
    4. ATS Improvement Suggestions

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