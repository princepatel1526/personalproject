import logging
import os
import traceback

import gspread
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from oauth2client.service_account import ServiceAccountCredentials

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


def save_to_google_sheets(data: dict) -> None:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Proposal Responses").sheet1
    row = [
        data.get("q1", ""),
        data.get("q2", ""),
        data.get("like_score", ""),
        data.get("final_response", ""),
    ]
    sheet.append_row(row)


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

    for item in QUESTION_BANK:
        answer = request.form.get(item["id"], "").strip()
        if not answer:
            flash("Please complete all steps before submitting.", "error")
            return redirect(url_for("questions"))

    like_score = request.form.get("like_score", "").strip()
    if not like_score.isdigit() or not (0 <= int(like_score) <= 100):
        flash("Please set the like score before submitting.", "error")
        return redirect(url_for("questions"))

    final_response = request.form.get("final_response", "").strip()
    if not final_response:
        flash("Please choose a final response.", "error")
        return redirect(url_for("questions"))

    form_data = dict(request.form)
    try:
        save_to_google_sheets(form_data)
    except Exception as e:
        print("SHEET ERROR:", e)
        traceback.print_exc()

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
