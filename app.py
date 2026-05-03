import logging
import os
import tempfile
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

from utils.email_sender import send_email_with_attachment
from utils.pdf_generator import generate_proposal_pdf

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY environment variable is not set.")

KNOW_YOU_OPTIONS = [
    "Your hidden fears",
    "Things that make you overthink",
    "Your favorite comfort things",
    "Something you’ve never told me",
    "What truly makes you happy",
]

QUESTION_BANK = [
    {"id": "q1", "text": "What do you genuinely feel when you talk to me?", "options": [
        {"text": "I feel happy and relaxed", "tone": "positive"},
        {"text": "I feel curious and interested", "tone": "positive"},
        {"text": "I enjoy it, but I don’t think much about it", "tone": "neutral"},
        {"text": "It feels different… in a good way", "tone": "positive"},
    ]},
    {"id": "q2", "text": "Do you think we could actually work as something more?", "options": [
        {"text": "Yes, I can see that", "tone": "positive"},
        {"text": "Maybe… I’m not sure yet", "tone": "neutral"},
        {"text": "I haven’t thought about it", "tone": "neutral"},
        {"text": "No, I don’t think so", "tone": "negative"},
    ]},
]
FINAL_OPTIONS = ["Yes ❤️", "No 😅", "I’ll tell you when you come to Mumbai 😉"]


@app.route("/")
def landing():
    return render_template("index.html")


@app.route("/know-you", methods=["GET", "POST"])
def know_you():
    if request.method == "POST":
        selected = request.form.getlist("know_you[]")
        valid_selected = [item for item in selected if item in KNOW_YOU_OPTIONS]
        session["know_you_choices"] = valid_selected
        return redirect(url_for("questions"))
    return render_template("know_you.html")


@app.route("/questions")
def questions():
    return render_template("questions.html", questions=QUESTION_BANK)


@app.route("/submit", methods=["POST"])
def submit():
    print("Form submitted successfully")
    print("Final response:", request.form.get("final_response"))
    print("FORM DATA:", request.form)
    recipient_email = os.getenv("RECIPIENT_EMAIL", "").strip()
    if not recipient_email:
        flash("Server configuration error: recipient email is not configured.", "error")
        return redirect(url_for("questions"))

    answers = []
    know_you_choices = session.get("know_you_choices", [])
    if know_you_choices:
        answers.append(("What is something about you that I don’t know yet?", ", ".join(know_you_choices)))

    for item in QUESTION_BANK:
        answer = request.form.get(item["id"], "").strip()
        if not answer:
            flash("Please complete all steps before submitting.", "error")
            return redirect(url_for("questions"))
        answers.append((item["text"], answer))

    like_score = request.form.get("like_score", "").strip()
    if not like_score.isdigit() or not (0 <= int(like_score) <= 100):
        flash("Please set the like score before submitting.", "error")
        return redirect(url_for("questions"))
    answers.append(("How much do you like me?", f"{like_score}%"))

    final_response = request.form.get("final_response", "").strip()
    if not final_response:
        flash("Please choose a final response.", "error")
        return redirect(url_for("questions"))
    answers.append(("Mansi Shukla… will you be mine?", final_response))

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

    print("Redirecting to final page")
    return redirect(url_for("final"))




@app.route("/final")
def final():
    return render_template("final.html")

@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
