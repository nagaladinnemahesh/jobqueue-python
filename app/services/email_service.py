import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def send_email(payload: dict):
    print("email function called")
    to_email = payload.get("to")
    subject = payload.get("subject", "No Subject")
    body = payload.get("body", "Empty email")

    if not to_email:
        raise Exception("No recipitent provided")
    
    if not payload:
        raise Exception("Payload missing")
    
    #gmail credentials
    sender_email = settings.EMAIL_SENDER
    app_password = settings.EMAIL_PASSWORD

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)

        print(f"[EMAIL SENT] to {to_email}")
    except Exception as e:
        raise Exception(f"Email failed: {str(e)}")