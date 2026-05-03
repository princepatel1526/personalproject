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
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `RECIPIENT_EMAIL`

Also add these if used in your SMTP setup:
- `SMTP_SERVER`
- `SMTP_PORT`

## 5) Common issues
- **Images not loading**
  - Ensure files are in `/static/images/`
  - Verify exact filename and case
- **Email not working**
  - Use valid SMTP credentials
  - For Gmail, use an app password
- **Case sensitivity on deployment**
  - `mansi1.jpg` and `Mansi1.jpg` are different on Linux

## 6) Final testing
1. Open the deployed link on your phone.
2. Complete `/know-you` and `/questions` flow.
3. Submit and verify the email is received with attached PDF.
