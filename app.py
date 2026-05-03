import os
import tempfile
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, flash

from utils.email_sender import send_email_with_attachment
from utils.pdf_generator import generate_proposal_pdf

load_dotenv()

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
    answers = []
    for i, question in enumerate(QUESTIONS, start=1):
        answer = request.form.get(f"q{i}", "").strip()
        if not answer:
            flash("Please answer all questions before submitting.", "error")
            return redirect(url_for("questions"))
        answers.append((question, answer))

    recipient_email = os.getenv("RECIPIENT_EMAIL")
    if not recipient_email:
        flash("Server configuration error: RECIPIENT_EMAIL is missing.", "error")
        return redirect(url_for("questions"))

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
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

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
