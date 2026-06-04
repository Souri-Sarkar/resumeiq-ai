from report_generator import generate_report
import streamlit as st
import requests
import pandas as pd

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

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
        )
    }

    data = {
        "job_description": job_description
    }

    with st.spinner("Analyzing Resume..."):

        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            files=files,
            data=data
        )

    result = response.json()

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

    history_response = requests.get(
        "http://127.0.0.1:8000/history"
    )

    history = history_response.json()

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

except:
    st.sidebar.write("No history found")