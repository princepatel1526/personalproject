import logging
import os
import base64

import resend

logger = logging.getLogger(__name__)


def send_email_with_attachment(recipient: str, subject: str, body: str, attachment_path: str) -> None:
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    sender = os.getenv("SENDER_EMAIL", "").strip()

    if not api_key:
        raise RuntimeError("RESEND_API_KEY environment variable is not set.")
    if not sender:
        raise RuntimeError("SENDER_EMAIL environment variable is not set.")

    resend.api_key = api_key

    with open(attachment_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    filename = os.path.basename(attachment_path)

    params = {
        "from": sender,
        "to": [recipient],
        "subject": subject,
        "text": body,
        "attachments": [
            {
                "filename": filename,
                "content": pdf_data,
            }
        ],
    }

    response = resend.Emails.send(params)
    logger.info("Email sent via Resend. ID: %s", response.get("id"))
