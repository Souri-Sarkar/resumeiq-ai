from backend.services.groq_service import get_resume_feedback

result = get_resume_feedback(
    "Python SQL Machine Learning",
    "Looking for Data Scientist with Python SQL"
)

print(result)