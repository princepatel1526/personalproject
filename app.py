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

QUESTIONS = [
    "What was the first moment you felt we shared something special?",
    "What do you love most about spending time with me?",
    "Which memory of us makes your heart smile the most?",
    "What dream would you love for us to build together?",
    "When life gets tough, how can we remind each other of our love?",
    "What does forever with me feel like to you?",
]


@app.route("/")
def landing():
    return render_template("index.html")


@app.route("/questions")
def questions():
    return render_template("questions.html", questions=QUESTIONS)


@app.route("/submit", methods=["POST"])
def submit():
    recipient_email = os.getenv("RECIPIENT_EMAIL", "").strip()
    if not recipient_email:
        logger.error("RECIPIENT_EMAIL is missing in environment configuration.")
        flash("Server configuration error: recipient email is not configured.", "error")
        return redirect(url_for("questions"))

    answers = []
    for i, question in enumerate(QUESTIONS, start=1):
        answer = request.form.get(f"q{i}", "").strip()
        if not answer:
            logger.warning("Validation failed: missing answer for question %s", i)
            flash("Please answer all questions before submitting.", "error")
            return redirect(url_for("questions"))
        answers.append((question, answer))

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, f"mansi_proposal_{timestamp}.pdf")

            generate_proposal_pdf(
                pdf_path=pdf_path,
                title="A Heartfelt Note for Mansi Shukla",
                qa_pairs=answers,
                closing_message=(
                    "Every answer tells one story: love that is gentle, honest, and eternal. "
                    "Mansi, may this be the beginning of our forever."
                ),
            )
            logger.info("PDF generated successfully at %s", pdf_path)

            send_email_with_attachment(
                recipient=recipient_email,
                subject="A Romantic Proposal for Mansi Shukla 💌",
                body=(
                    "Hello,\n\n"
                    "Please find attached the romantic proposal responses in PDF format.\n"
                    "This message was sent from the Flask Romantic Proposal App.\n\n"
                    "With love,\n"
                    "Your Proposal Website"
                ),
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
