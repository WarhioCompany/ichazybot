from email.message import EmailMessage
import ssl, smtplib

email_sender = 'warhiocodetest@gmail.com'
email_pass = 'hgegikakxnnfnngo'


def send(email_receiver, subject, content):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
