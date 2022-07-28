import sendgrid

from sendgrid.helpers.mail import Mail, Email, To, Content, Subject
from python_http_client.client import Response

from app.core import config


def send_email(to_email: str, subject: str, content: str) -> Response:
    sg = sendgrid.SendGridAPIClient(api_key=config.SENDGRID_API_KEY)
    mail = Mail(
        from_email=Email(config.FROM_EMAIL),
        to_emails=To(to_email),
        subject=Subject(subject),
        plain_text_content=Content("text/plain", content)
    )
    mail_json = mail.get()
    return sg.client.mail.send.post(request_body=mail_json)
