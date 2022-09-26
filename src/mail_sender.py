from redmail import EmailSender


def sendMail(destination):
    email = EmailSender(
        host="mail.sbop.com.br",
        port=25,
        username="noreply@sbop.com.br",
        password="oht#yoYNO^R2"
    )

    email.send(
        sender="noreply@sbop.com.br",
        receivers=[destination],
        subject="Sbop - Recuperar senha",
        # text="Hi, this is text body.",
        html="<h1>Hi,</h1><p>this is HTML body</p>"
    )
    