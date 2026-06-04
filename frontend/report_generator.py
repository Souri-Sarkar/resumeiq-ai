from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(result, filename):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("ResumeIQ AI Report", styles["Title"])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"ATS Score: {result['ats_score']}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Semantic Score: {result['semantic_score']}%",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Skills Found:",
            styles["Heading2"]
        )
    )

    for skill in result["skills_found"]:
        content.append(
            Paragraph(f"• {skill}", styles["Normal"])
        )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "AI Feedback:",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            result["ai_feedback"],
            styles["Normal"]
        )
    )

    pdf.build(content)