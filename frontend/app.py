from report_generator import generate_report
import streamlit as st
import pandas as pd
import tempfile
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from backend.resume_parser import extract_text_from_pdf
from backend.ats_engine import calculate_ats_score
from backend.services.skills import extract_skills
from backend.services.groq_service import get_resume_feedback
from backend.services.section_checker import check_resume_sections
from backend.services.semantic_match import semantic_similarity
from backend.history import save_analysis, get_history

st.set_page_config(
    page_title="ResumeIQ AI",
    page_icon="📄",
    layout="wide"
)

# Sidebar
st.sidebar.title("📄 ResumeIQ AI")

st.sidebar.markdown("""
### Features

✅ ATS Score

✅ Semantic Matching

✅ Skill Extraction

✅ Keyword Matching

✅ Resume Section Analysis

✅ AI Recruiter Feedback
""")

   # Main Title
st.title("📄 ResumeIQ AI")
st.subheader("AI-Powered Resume Analyzer")

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# Job Description
job_description = st.text_area(
    "Paste Job Description"
)

# Analyze Button
if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        with st.spinner("Analyzing Resume..."):

            # Save uploaded PDF temporarily
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            )

            temp_file.write(uploaded_file.getvalue())
            temp_file.close()

            # Extract Resume Text
            resume_text = extract_text_from_pdf(
                temp_file.name
            )

            # Delete temporary file
            os.unlink(temp_file.name)

            # ATS Score
            ats_result = calculate_ats_score(
                resume_text,
                job_description
            )

        # Skills
        skills_found = extract_skills(
            resume_text
        )

        # Resume Sections
        sections = check_resume_sections(
            resume_text
        )

        # Semantic Matching
        semantic_score = semantic_similarity(
            resume_text,
            job_description
        )

        # AI Feedback
        ai_feedback = get_resume_feedback(
            resume_text,
            job_description
        )

        # Save History
        save_analysis({
            "filename": uploaded_file.name,
            "ats_score": ats_result["score"],
            "semantic_score": semantic_score
        })

        # Final Result Dictionary
        result = {
            "filename": uploaded_file.name,
            "ats_score": ats_result["score"],
            "semantic_score": semantic_score,
            "matched_keywords": ats_result["matched_keywords"],
            "missing_keywords": ats_result["missing_keywords"],
            "skills_found": skills_found,
            "sections_found": sections["found"],
            "sections_missing": sections["missing"],
            "ai_feedback": ai_feedback
        }

        st.success("Analysis Complete")

        # Scores

        st.subheader("📊 Resume Analysis Scores")

        col1, col2 = st.columns(2)

        with col1:
            ats_score = result["ats_score"]

            st.metric(
                "ATS Score",
                f"{ats_score}%"
            )

            st.progress(ats_score / 100)

        with col2:
            semantic_score = result["semantic_score"]

            st.metric(
                "Semantic Match",
                f"{semantic_score}%"
            )

            st.progress(semantic_score / 100)

        # Keywords

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Keywords")

            for keyword in result["matched_keywords"]:
                st.success(keyword)

        with col2:
            st.subheader("❌ Missing Keywords")

            for keyword in result["missing_keywords"]:
                st.error(keyword)

        # Skills

        st.subheader("🛠 Skills Found")

        skills_cols = st.columns(3)

        for i, skill in enumerate(result["skills_found"]):
            with skills_cols[i % 3]:
                st.info(skill)

        # Resume Sections

        st.subheader("📑 Resume Sections")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("✅ Found")

            for section in result["sections_found"]:
                st.success(section.title())

        with col4:
            st.subheader("❌ Missing")

            for section in result["sections_missing"]:
                st.error(section.title())

        # AI Feedback

        st.subheader("🤖 AI Recruiter Feedback")

        st.markdown(result["ai_feedback"])

        report_file = "resume_report.pdf"

        generate_report(
            result,
            report_file
        )

        with open(report_file, "rb") as file:

            st.download_button(
                label="📥 Download ATS Report",
                data=file,
                file_name="ResumeIQ_Report.pdf",
                mime="application/pdf"
        )
    else:
        st.warning(
            "Please upload a resume and enter a job description."
        )
    st.sidebar.subheader("📜 Previous Analyses")

    try:

        history = get_history()

        if history:

            for item in reversed(history[-5:]):

                st.sidebar.write(
                    f"📄 {item['filename']}"
                )

                st.sidebar.caption(
                    f"ATS: {item['ats_score']}% | Semantic: {item['semantic_score']}%"
                )

            # Analytics
            st.sidebar.subheader("📊 Analytics")

            df = pd.DataFrame(history)

            st.sidebar.metric(
                "Total Analyses",
                len(df)
            )

            st.sidebar.metric(
                "Average ATS",
                round(df["ats_score"].mean(), 2)
            )

            st.sidebar.metric(
                "Average Semantic",
                round(df["semantic_score"].mean(), 2)
            )

        else:
            st.sidebar.write("No history found")

    except Exception:
        st.sidebar.write("No history found")