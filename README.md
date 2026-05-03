# Romantic Proposal Website (Flask)

A responsive romantic proposal website dedicated to **Mansi Shukla**, built from scratch using Flask, HTML, CSS, and JavaScript.

## Features
- Romantic landing page with card layout and animations
- Multi-step romantic questionnaire with client-side validation
- Flask backend submission handler
- Structured PDF generation with all questions and answers
- Real SMTP email delivery with PDF attachment
- Final proposal page with typewriter effect and optional music toggle

## Project Structure

```
.
├── app.py
├── requirements.txt
├── .env.example
├── templates/
│   ├── index.html
│   ├── questions.html
│   └── success.html
├── static/
│   ├── css/styles.css
│   ├── js/main.js
│   └── images/hero.svg
└── utils/
    ├── email_sender.py
    └── pdf_generator.py
```

## Setup Instructions

1. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create your environment file**
   ```bash
   cp .env.example .env
   ```

4. **Configure SMTP credentials in `.env`**
   - `SMTP_SERVER`: SMTP host (e.g., `smtp.gmail.com`)
   - `SMTP_PORT`: Usually `587`
   - `SMTP_USERNAME`: SMTP login username (**also used as sender email**)
   - `SMTP_PASSWORD`: SMTP password/app password
     - `RECIPIENT_EMAIL`: Address receiving the proposal PDF

   > For Gmail, use an **App Password** if 2FA is enabled.

5. **Run the app**
   ```bash
   python app.py
   ```

6. **Open in browser**
   - Visit `http://127.0.0.1:5000`

## Flow
1. Open landing page (`/`)
2. Click **Enter**
3. Fill all romantic questions (`/questions`)
4. Submit to trigger:
   - PDF generation
   - SMTP email with PDF attachment
5. Redirect to final proposal page (`/success`)

