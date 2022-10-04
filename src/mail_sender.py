from redmail import EmailSender
from pathlib import Path


def sendMail(destination, subject, message, attachment = None):
    email = EmailSender(
        host="mail.sbop.com.br",
        port=25,
        username="noreply@sbop.com.br",
        password="oht#yoYNO^R2"
    )

    email.send(
        sender="noreply@sbop.com.br",
        receivers=[destination],
        subject=subject,
        text=message,
        # html="<h1>Olá,</h1><p>this is HTML body</p>"
        attachments = {
            attachment['filename']: Path(attachment['path'])
        } if attachment else None
    )
    