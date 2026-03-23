import smtplib, ssl, os
from dotenv import load_dotenv
load_dotenv()

smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", 587))
p1_gmail = os.getenv("PERFIL_1_GMAIL_EMAIL", "NOT SET")
p1_pass = os.getenv("PERFIL_1_GMAIL_APP_PASS", "NOT SET")

print(f"SMTP: {smtp_server}:{smtp_port}")
print(f"Gmail: {p1_gmail}")
print(f"Pass length: {len(p1_pass)} chars")

print("Testing SMTP connection...")
try:
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(p1_gmail, p1_pass)
        print("SUCCESS: Login OK - SMTP funciona correctamente")
except Exception as e:
    print(f"ERROR: {e}")
