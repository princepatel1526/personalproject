import os
import requests


def send_email_resend(recipient: str, subject: str, body: str) -> None:
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    sender = os.getenv("SENDER_EMAIL", "onboarding@resend.dev").strip()

    if not api_key:
        raise RuntimeError("RESEND_API_KEY environment variable is not set.")

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": sender,
            "to": [recipient],
            "subject": subject,
            "text": body,
        },
        timeout=30,
    )
    response.raise_for_status()
