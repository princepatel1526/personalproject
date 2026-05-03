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
    {"id": "q1", "text": "How do you feel when we talk?", "options": [
        {"text": "Happy and calm", "tone": "positive"}, {"text": "Excited and nervous", "tone": "positive"},
        {"text": "Safe and understood", "tone": "positive"}, {"text": "It depends on the day", "tone": "neutral"}]},
    {"id": "q2", "text": "Which moment with me feels most magical?", "options": [
        {"text": "Late-night conversations", "tone": "positive"}, {"text": "Our laughter together", "tone": "positive"},
        {"text": "Simple walks together", "tone": "positive"}, {"text": "I am still figuring it out", "tone": "neutral"}]},
    {"id": "q3", "text": "What do you treasure most about us?", "options": [
        {"text": "Our emotional comfort", "tone": "positive"}, {"text": "Our deep trust", "tone": "positive"},
        {"text": "Our shared dreams", "tone": "positive"}, {"text": "I need more time to know", "tone": "negative"}]},
    {"id": "q4", "text": "If love had a color for us, it would be...", "options": [
        {"text": "Soft pink like tenderness", "tone": "positive"}, {"text": "Golden like warm sunsets", "tone": "positive"},
        {"text": "Blue like peaceful skies", "tone": "neutral"}, {"text": "I cannot pick one", "tone": "neutral"}]},
    {"id": "q5", "text": "What do you hope for our future?", "options": [
        {"text": "A forever friendship and love", "tone": "positive"}, {"text": "Growing old hand in hand", "tone": "positive"},
        {"text": "A life of adventure", "tone": "neutral"}, {"text": "I am not sure yet", "tone": "negative"}]},
]


@app.route("/")
def landing():
    return render_template("index.html")


@app.route("/questions")
def questions():
    return render_template("questions.html", questions=QUESTION_BANK)


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
        valid_options = [option["text"] for option in item["options"]]
        if answer not in valid_options:
            logger.warning("Validation failed for %s. Received invalid answer: %s", item["id"], answer)
            flash("Please select one option for each question.", "error")
            return redirect(url_for("questions"))
        answers.append((item["text"], answer))

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, f"mansi_proposal_{timestamp}.pdf")
            generate_proposal_pdf(pdf_path=pdf_path, title="A Heartfelt Note for Mansi Shukla", qa_pairs=answers, closing_message="Every chosen answer feels like a heartbeat saying yes to love.")
            send_email_with_attachment(
                recipient=recipient_email,
                subject="A Romantic Proposal for Mansi Shukla 💌",
                body="Hello,\n\nPlease find attached the romantic proposal responses in PDF format.\n\nWith love,\nYour Proposal Website",
                attachment_path=pdf_path,
            )
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
