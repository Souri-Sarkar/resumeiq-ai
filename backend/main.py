from fastapi import FastAPI, UploadFile, File, Form
from backend.resume_parser import extract_text_from_pdf
from backend.ats_engine import calculate_ats_score
from backend.services.skills import extract_skills
from backend.services.groq_service import get_resume_feedback
from backend.services.section_checker import check_resume_sections
from backend.services.semantic_match import semantic_similarity
from backend.history import save_analysis,get_history

import tempfile
import os

app = FastAPI(
    title="ResumeIQ AI",
    description="AI-Powered Resume Analyzer",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "ResumeIQ AI Backend Running"
    }

@app.get("/history")
def history():
    return get_history()

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Save uploaded PDF temporarily
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    content = await file.read()

    temp_file.write(content)
    temp_file.close()

    # Extract text
    resume_text = extract_text_from_pdf(
        temp_file.name
    )

    # Delete temp file
    os.unlink(temp_file.name)

    # ATS Score
    result = calculate_ats_score(
        resume_text,
        job_description
    )

    # Skills Extraction
    skills_found = extract_skills(
        resume_text
    )
    sections = check_resume_sections(
    resume_text
)
    semantic_score = semantic_similarity(
    resume_text,
    job_description
)
    # Groq AI Feedback
    ai_feedback = get_resume_feedback(
        resume_text,
        job_description
    )
    save_analysis({
        "filename": file.filename,
        "ats_score": result["score"],
        "semantic_score": semantic_score
    })
    
    return {
    "filename": file.filename,
    "ats_score": result["score"],
    "semantic_score": semantic_score,
    "matched_keywords": result["matched_keywords"],
    "missing_keywords": result["missing_keywords"],
    "skills_found": skills_found,
    "sections_found": sections["found"],
    "sections_missing": sections["missing"],
    "ai_feedback": ai_feedback
}