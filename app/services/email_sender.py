import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate, make_msgid
from app.config import Config

class EmailSender:
    def __init__(self, smtp_server=None, smtp_port=None):
        self.smtp_server = smtp_server or Config.SMTP_SERVER
        self.smtp_port = smtp_port or Config.SMTP_PORT
        self.context = ssl.create_default_context()

    def send(self, sender_data, recipient_data, subject, html_body, logo_path=None):
        """
        Envía un correo electrónico individual.
        sender_data: dict {email, password, nombre, cargo}
        recipient_data: dict {email, nombre}
        """
        try:
            message = MIMEMultipart("related")
            message["Subject"] = subject
            message["From"] = sender_data["email"]
            message["To"] = recipient_data["email"]
            message["Date"] = formatdate(localtime=True)
            message["Message-ID"] = make_msgid(domain="partnertech.pe")
            message["List-Unsubscribe"] = "<mailto:negocios@partnertech.pe?subject=unsubscribe>"
            
            msg_alternative = MIMEMultipart("alternative")
            message.attach(msg_alternative)
            
            # Texto plano de respaldo
            text_plain = f"Hola {recipient_data['nombre']},\n\nGracias por tu interés en Partner Tech.\n\nAtentamente,\n{sender_data['nombre']}"
            msg_alternative.attach(MIMEText(text_plain, "plain"))
            msg_alternative.attach(MIMEText(html_body, "html"))
            
            # Adjuntar logo si existe
            if logo_path:
                try:
                    with open(logo_path, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-ID', '<Logo_ver1>')
                        message.attach(img)
                except Exception as e:
                    logging.warning(f"No se pudo adjuntar el logo: {e}")
            
            # Conexión y envío
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=self.context) as server:
                server.login(sender_data["email"], sender_data["password"])
                server.sendmail(sender_data["email"], recipient_data["email"], message.as_string())
            
            return True, "Enviado"
        except Exception as e:
            error_msg = str(e)
            logging.error(f"Error enviando a {recipient_data['email']}: {error_msg}")
            return False, error_msg
