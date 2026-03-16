import os
import smtplib
import ssl
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate, make_msgid
from datetime import datetime

# --- CONFIGURACIÓN ---
SMTP_SERVER = "mail.partnertech.pe"
SMTP_PORT = 465
SENDER_EMAIL = "fguerrero@partnertech.pe"
SENDER_PASS = "Franco001"
DEST_EMAILS = [
    "guerrerofranco1429@gmail.com",
    "negocios@partnertech.pe",
    "acardozo@partnertech.pe"
]

TEMPLATES = [
    {
        "name": "Base Stitch A (Final - Firma Alineada)",
        "file": "templates/base/base_diseno_a.html",
        "vars": {
            "Titulo_Pagina": "Partner Tech | Gestión Médica Inteligente",
            "Nombre_Producto": "Solución de Gestión Médica",
            "Asunto_Override": "Tu Socio Estratégico: Solución de Gestión Médica",
            "Nombre_Contacto": "Doctor",
            "CTA_Link": "https://cal.com/negocios-partner-tech/requerimientos-software-desarrollo",
            "Campana": "produccion_ccl_v1",
            "Nombre_Remitente": "Franco Guerrero",
            "Cargo_Remitente": "Director Comercial",
            "Email_Remitente": "fguerrero@partnertech.pe",
            "Email_Destinatario": "{{Email_Destinatario}}",
            "Email_Hash": "{{Email_Hash}}"
        }
    },
    {
        "name": "Base Stitch B (Final - Firma Alineada)",
        "file": "templates/base/base_diseno_b.html",
        "vars": {
            "Titulo_Pagina": "Partner Tech | Soberanía Tecnológica",
            "Asunto_Override": "Tu Socio Estratégico: Optimización Operativa Policlínicos",
            "Nombre_Contacto": "Doctor",
            "CTA_Link": "https://partnertech.pe",
            "Campana": "produccion_ccl_v1",
            "Nombre_Remitente": "Franco Guerrero",
            "Cargo_Remitente": "Director Comercial",
            "Email_Remitente": "fguerrero@partnertech.pe",
            "Email_Destinatario": "{{Email_Destinatario}}",
            "Email_Hash": "{{Email_Hash}}"
        }
    }
]

def send_email(template_config, dest_email):
    try:
        with open(template_config["file"], "r", encoding="utf-8") as f:
            html = f.read()
        
        # Preparar variables específicas para el destinatario
        email_hash = hashlib.md5(dest_email.encode()).hexdigest()
        
        for key, val in template_config["vars"].items():
            content = str(val)
            if key == "Email_Destinatario": content = dest_email
            if key == "Email_Hash": content = email_hash
            html = html.replace(f"{{{{{key}}}}}", content)

        msg = MIMEMultipart("related")
        # Identificador de plantilla para el asunto (A o B)
        template_id = "Plantilla A" if "base_diseno_a" in template_config["file"] else "Plantilla B"
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg["Subject"] = f"{template_id} | {timestamp}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = dest_email
        msg["Date"] = formatdate(localtime=True)
        msgid = make_msgid(domain="partnertech.pe")
        msg["Message-ID"] = msgid
        # Cabecera para ayudar a Gmail a no agrupar en hilos
        msg["X-Entity-Ref-ID"] = msgid

        msg_alt = MIMEMultipart("alternative")
        msg.attach(msg_alt)
        msg_alt.attach(MIMEText(html, "html"))

        # Mapeo de activos (CIDs DEBEN COINCIDIR CON EL HTML)
        assets = [
            ("assets/logos/logo_color.png", "logo_oficial"),
            ("assets/logos/Logo_y_texto_Partner_Tech.png", "Logo_Color"), 
            ("assets/icons/custom/agenda_red.png", "minimalist_agenda_red"),
            ("assets/icons/custom/history_green.png", "minimalist_history_green"),
            ("assets/icons/custom/agenda_navy.png", "minimalist_agenda_navy"),
            ("assets/icons/custom/history_navy.png", "minimalist_history_navy"),
            ("assets/icons/custom/finance_navy.png", "minimalist_finance_navy"),
            ("assets/icons/custom/whatsapp_white.png", "whatsapp_blanco"),
            ("assets/icons/icomoon/401-facebook.png", "soc_fb"),
            ("assets/icons/icomoon/403-instagram.png", "soc_ig"),
            ("assets/icons/icomoon/458-linkedin.png", "soc_li")
        ]

        for path, cid in assets:
            # SOLO ADJUNTAR SI SE USA EN EL HTML
            if f"cid:{cid}" in html:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        img = MIMEImage(f.read())
                        img.add_header("Content-ID", f"<{cid}>")
                        # NO agregamos Content-Disposition ni filename para evitar que se vean como adjuntos
                        msg.attach(img)
                else:
                    print(f"⚠️ Advertencia: No se encontró el activo {path}")

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.sendmail(SENDER_EMAIL, [dest_email], msg.as_string())
        
        print(f"✅ Enviado: {template_config['name']} -> {dest_email}")
    except Exception as e:
        print(f"❌ Error en {template_config['name']}: {e}")

if __name__ == "__main__":
    print(f"🚀 Iniciando envío de prueba a {len(DEST_EMAILS)} destinatarios...")
    for email in DEST_EMAILS:
        for t in TEMPLATES:
            send_email(t, email)
