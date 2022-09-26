from src.config import email as config
from redmail import EmailSender

def sendMail(email):
    email = EmailSender(
        host=config['host'],
        port=config['port'],
        username=config['login'],
        password=config['password']
    )

    email.send(
        sender=config['login'],
        receivers=[email],
        subject="Sbop - Recuperar senha",
        # text="Hi, this is text body.",
        html="<h1>Hi,</h1><p>this is HTML body</p>"
    )
    