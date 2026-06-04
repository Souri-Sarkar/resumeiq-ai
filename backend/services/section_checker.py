SECTIONS = [
    "education",
    "skills",
    "projects",
    "experience",
    "certification",
    "certifications"
]

def check_resume_sections(resume_text):

    resume_text = resume_text.lower()

    found = []
    missing = []

    for section in SECTIONS:

        if section in resume_text:
            found.append(section)
        else:
            missing.append(section)

    return {
        "found": found,
        "missing": missing
    }