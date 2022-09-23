# from src.config import email as config
# import yagmail

# def sendMail(destination, subject, message):
#     print(config['login'], config['password'])
#     yag = yagmail.SMTP(config['login'], config['password'])
#     yag.send(destination, subject, message)

import smtplib

#Ports 465 and 587 are intended for email client to email server communication - sending email
server = smtplib.SMTP('mail.sbop.com.br', 587)

#starttls() is a way to take an existing insecure connection and upgrade it to a secure connection using SSL/TLS.
server.starttls()

#Next, log in to the server
server.login("noreply@sbop.com.br", "oht#yoYNO^R2")

msg = "TESTE"

#Send the mail
server.sendmail("noreply@sbop.com.br", "fernando@agenciazop.com.br", msg)