# from src.config import email as config
from redmail import EmailSender

email = EmailSender(
    host="mail.sbop.com.br",
    port=25,
    user_name="noreply@sbop.com.br",
    password="oht#yoYNO^R2"
)

email.send(
    sender="noreply@sbop.com.br",
    receivers=["fernando@agenciazop.com.br"],
    subject="An example email",
    text="Hi, this is text body.",
    html="<h1>Hi,</h1><p>this is HTML body</p>"
)