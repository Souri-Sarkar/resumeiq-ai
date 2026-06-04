import re

STOPWORDS = {
    "a", "an", "the", "and", "or",
    "with", "for", "to", "of",
    "in", "on", "at", "is", "are",
    "looking"
}

def calculate_ats_score(resume_text, job_description):

    resume_words = {
        word
        for word in re.findall(r'\w+', resume_text.lower())
        if len(word) > 2 and word not in STOPWORDS
    }

    jd_words = {
        word
        for word in re.findall(r'\w+', job_description.lower())
        if len(word) > 2 and word not in STOPWORDS
    }

    if len(jd_words) == 0:
        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": []
        }

    matched = resume_words.intersection(jd_words)

    missing = jd_words - resume_words

    score = round(
        (len(matched) / len(jd_words)) * 100,
        2
    )

    return {
        "score": score,
        "matched_keywords": sorted(list(matched)),
        "missing_keywords": sorted(list(missing))
    }