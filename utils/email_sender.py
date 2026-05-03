import logging
import os
import smtplib
import ssl
from email.message import EmailMessage

logger = logging.getLogger(__name__)


def send_email_with_attachment(recipient: str, subject: str, body: str, attachment_path: str) -> None:
    smtp_server = os.getenv("SMTP_SERVER", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "")

    sender_email = smtp_username

    required = [smtp_server, smtp_username, smtp_password, recipient]
    if not all(required):
        raise RuntimeError("Missing SMTP/recipient configuration in environment variables.")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    if not os.path.isfile(attachment_path):
        raise FileNotFoundError(f"Attachment file not found: {attachment_path}")

    with open(attachment_path, "rb") as file:
        pdf_data = file.read()

    msg.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=os.path.basename(attachment_path),
    )

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError as exc:
        logger.error(
            "SMTP authentication failed. For Gmail, ensure 2FA is enabled and SMTP_PASSWORD is an app password."
        )
        raise RuntimeError("SMTP authentication failed. Check SMTP_USERNAME and SMTP_PASSWORD.") from exc
    except smtplib.SMTPException as exc:
        logger.error("SMTP error while sending email: %s", exc)
        raise RuntimeError(f"SMTP error while sending email: {exc}") from exc
