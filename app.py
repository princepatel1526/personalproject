import logging
import os
import tempfile
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from utils.email_sender import send_email_with_attachment
from utils.pdf_generator import generate_proposal_pdf

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-me-in-production")

QUESTION_BANK = [
    {
        "id": "q1",
        "text": "How do you feel when we talk?",
        "options": ["Happy and calm", "Excited and nervous", "Safe and understood", "Like time stops"],
    },
    {
        "id": "q2",
        "text": "Which moment with me feels most magical?",
        "options": ["Late-night conversations", "Our laughter together", "Silent eye contact", "Simple walks together"],
    },
    {
        "id": "q3",
        "text": "What do you treasure most about us?",
        "options": ["Our emotional comfort", "Our playful bond", "Our deep trust", "Our shared dreams"],
    },
    {
        "id": "q4",
        "text": "If love had a color for us, it would be...",
        "options": ["Soft pink like tenderness", "Golden like warm sunsets", "Blue like peaceful skies", "Crimson like passion"],
    },
    {
        "id": "q5",
        "text": "What do you hope for our future?",
        "options": ["A home full of laughter", "A life of adventure", "A forever friendship and love", "Growing old hand in hand"],
    },
]


@app.route("/")
def landing():
    return render_template("index.html")


@app.route("/questions")
def questions():
    return render_template("questions.html", questions=QUESTION_BANK, total_questions=len(QUESTION_BANK))


@app.route("/submit", methods=["POST"])
def submit():
    recipient_email = os.getenv("RECIPIENT_EMAIL", "").strip()
    if not recipient_email:
        logger.error("RECIPIENT_EMAIL is missing in environment configuration.")
        flash("Server configuration error: recipient email is not configured.", "error")
        return redirect(url_for("questions"))

    answers = []
    for item in QUESTION_BANK:
        answer = request.form.get(item["id"], "").strip()
        if answer not in item["options"]:
            logger.warning("Validation failed for %s. Received invalid answer: %s", item["id"], answer)
            flash("Please select one option for each question.", "error")
            return redirect(url_for("questions"))
        answers.append((item["text"], answer))

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, f"mansi_proposal_{timestamp}.pdf")

            generate_proposal_pdf(
                pdf_path=pdf_path,
                title="A Heartfelt Note for Mansi Shukla",
                qa_pairs=answers,
                closing_message="Every chosen answer feels like a heartbeat saying yes to love.",
            )
            logger.info("PDF generated successfully at %s", pdf_path)

            send_email_with_attachment(
                recipient=recipient_email,
                subject="A Romantic Proposal for Mansi Shukla 💌",
                body="Hello,\n\nPlease find attached the romantic proposal responses in PDF format.\n\nWith love,\nYour Proposal Website",
                attachment_path=pdf_path,
            )
            logger.info("Proposal email sent successfully to %s", recipient_email)

    except Exception:
        logger.exception("Submission processing failed.")
        flash("Sorry, something went wrong while sending your proposal. Please try again.", "error")
        return redirect(url_for("questions"))

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
