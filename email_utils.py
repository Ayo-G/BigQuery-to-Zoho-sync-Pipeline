import smtplib
from email.mime.text import MIMEText

def send_alert_email(function_name, error_message, traceback_str):
    sender_email = "SENDER EMAIL"
    receiver_email = "RECIEVER EMAIL" 
    app_password = "APP PASSWORD"

    subject = f"[ALERT] {function_name} sync failed"
    body = f"""
    ⚠️ Zohosheet Sync Failure Alert ⚠️
    
    Hi there,
    It looks like there has been an error with a function in the pipeline.
    
    Function: {function_name}
    Error Message: {error_message}

    Stack Trace:
    {traceback_str}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"📧 Alert email sent for {function_name}")
    except Exception as e:
        print(f"❌ Failed to send alert email: {str(e)}")
