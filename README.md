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



## Manual image placeholders for /know-you
Add your own images to `static/images/` with these filenames before running the full visual flow:
- `mansi1.jpg`
- `mansi2.jpg`
- `mansi3.jpg`
- `mansi4.jpg`
- `mansi5.jpg`

## How to Make Images and Animations Work

1. Folder structure:
   ```
   static/
     images/
   ```

2. Add your images manually:
   - `mansi1.jpg`
   - `mansi2.jpg`
   - `mansi3.jpg`
   - `mansi4.jpg`
   - `mansi5.jpg`
   - `mansi6.jpg`
   - `mansi7.jpg`

3. Use this format in HTML:
   ```html
   <img src="{{ url_for('static', filename='images/mansi1.jpg') }}" loading="lazy">
   ```

4. Make sure:
   - Images are inside `/static/images/`
   - Filenames match exactly (case-sensitive)
   - Images are optimized (small file size)

5. If images do not show:
   - Check path
   - Restart Flask server
   - Clear browser cache

6. Animation note:
   - Animations only apply if elements are visible
   - Ensure CSS classes are applied correctly
   - Check console for errors


## Common Issues & Fixes

- **Form not submitting** → Check that `static/js/main.js` is loading in the page and browser console has no JS errors.
- **500 error on /submit** → Check application logs for `PDF ERROR` and `EMAIL ERROR` tracebacks.
- **Email not sending** → Verify email provider env variables are correct in deployment settings.
- **Static files not loading** → Confirm lowercase folder names (`static/js`, `static/css`) and correct `url_for('static', ...)` paths.
