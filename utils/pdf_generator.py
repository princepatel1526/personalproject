from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_proposal_pdf(pdf_path: str, title: str, qa_pairs: list[tuple[str, str]], closing_message: str) -> None:
    if not qa_pairs:
        raise ValueError("Cannot generate PDF: no question/answer data provided.")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        textColor=colors.HexColor("#b44a6d"),
        fontSize=24,
        leading=30,
        alignment=1,
    )
    question_style = ParagraphStyle(
        "QuestionStyle",
        parent=styles["Heading3"],
        textColor=colors.HexColor("#8c3854"),
        fontSize=13,
        leading=18,
    )
    answer_style = ParagraphStyle(
        "AnswerStyle",
        parent=styles["BodyText"],
        fontSize=11,
        leading=17,
    )

    story = [
        Paragraph(title, title_style),
        Spacer(1, 0.3 * cm),
        Paragraph(f"Created on {datetime.now().strftime('%B %d, %Y at %H:%M')}", styles["Italic"]),
        Spacer(1, 0.6 * cm),
    ]

    for index, (question, answer) in enumerate(qa_pairs, start=1):
        story.append(Paragraph(f"{index}. {question}", question_style))
        story.append(Spacer(1, 0.15 * cm))
        story.append(Paragraph(answer, answer_style))
        story.append(Spacer(1, 0.45 * cm))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Closing Note", question_style))
    story.append(Spacer(1, 0.15 * cm))
    story.append(Paragraph(closing_message, answer_style))

    doc.build(story)
