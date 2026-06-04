SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "nlp",
    "power bi",
    "statistics",
    "data science",
    "data analysis"
]

def extract_skills(resume_text):

    resume_text = resume_text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in resume_text:
            found_skills.append(skill)

    return found_skills


def match_skills(resume_text, jd_text):

    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    matched = []
    missing = []

    for skill in SKILLS:
        if skill in jd_text:
            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

    return matched, missing