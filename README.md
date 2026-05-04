# Romantic Proposal Website (Flask)

A responsive romantic proposal website dedicated to **Mansi Shukla**, built from scratch using Flask, HTML, CSS, and JavaScript.

## Features
- Romantic landing page with card layout and animations
- Multi-step romantic questionnaire with client-side validation
- Flask backend submission handler
- Google Sheets storage of all questionnaire responses
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

4. **Add Google service account credentials**
   - Place `credentials.json` in project root
   - Share sheet `Proposal Responses` with service account email

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
4. Submit to store responses in Google Sheets
5. Redirect to final proposal page (`/final`)



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
- **Sheet write failing** → Verify `credentials.json`, sheet sharing permissions, and Google API enablement.
- **Static files not loading** → Confirm lowercase folder names (`static/js`, `static/css`) and correct `url_for('static', ...)` paths.


## Google Sheets Integration

1. Create a Google Sheet named **Proposal Responses**.
2. Enable Google Sheets API in your Google Cloud project.
3. Create a Service Account.
4. Download `credentials.json`.
5. Share the sheet with the service account email.
6. Place `credentials.json` in the project root.


## Google Sheets (Production Setup)

1. Open `credentials.json`.
2. Copy the entire JSON content.
3. Add it in Render environment variable: `GOOGLE_CREDS_JSON`.
4. Deploy (or redeploy) the app.
