# Deployment Guide

## 1) Push project to GitHub
1. Create a GitHub repository.
2. Commit and push this project branch:
   ```bash
   git add .
   git commit -m "Prepare Flask proposal app for deployment"
   git push origin main
   ```

## 2) Deploy using Render
1. Go to https://render.com
2. Create an account and log in.
3. Click **New +** → **Web Service**.
4. Connect your GitHub repository.

## 3) Build settings
Use these settings in Render:

- **Build command**
  ```bash
  pip install -r requirements.txt
  ```

- **Start command**
  ```bash
  gunicorn app:app
  ```

## 4) Environment variables
In Render service settings, add:

- `FLASK_SECRET_KEY`

## 5) Common issues
- **Images not loading**
  - Ensure files are in `/static/images/`
  - Verify exact filename and case
- **Google Sheets not writing**
  - Ensure `credentials.json` is present and readable
  - Ensure target sheet is shared with service account email
  - Ensure Google Sheets API is enabled
- **Case sensitivity on deployment**
  - `mansi1.jpg` and `Mansi1.jpg` are different on Linux

## 6) Final testing
1. Open the deployed link on your phone.
2. Complete `/know-you` and `/questions` flow.
3. Submit and verify the email is received with attached PDF.


## Deployment Troubleshooting

1. **Check Render logs**
   - Open your service in Render and inspect runtime logs during `/submit`.
2. **Verify POST /submit**
   - Use browser DevTools Network tab and confirm POST status + redirect target.
3. **Test static files manually**
   - Open `/static/js/main.js` and `/static/css/styles.css` directly from deployed URL.
4. **Verify environment variables**
   - Ensure all required keys are set exactly and without extra whitespace.
5. **Production vs local differences**
   - In production, HTTPS/proxy/env config can expose validation or provider issues not seen locally.


## Render Setup for Google Sheets

- Upload `credentials.json` OR provide equivalent secure file handling in your environment.
- Ensure credentials file is accessible in production runtime.
- Verify Google Sheets API access before testing submissions.


## Google Sheets on Render

- `credentials.json` will **not** be available in production filesystem.
- Use environment variable `GOOGLE_CREDS_JSON` instead.
- Ensure the JSON is pasted correctly as a single valid JSON value.
- Restart the service after adding/updating the variable.
