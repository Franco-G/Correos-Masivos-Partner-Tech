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
DEST_EMAIL = "guerrerofranco1429@gmail.com"

TEMPLATES = [
    {
        "name": "Base Stitch A (Final - Firma Alineada)",
        "file": "templates/base/base_diseno_a.html",
        "vars": {
            "Titulo_Pagina": "Clinic Mentor Pro | Gestión Inteligente",
            "Asunto_Override": "Socios CCL: Solución de Gestión para su Clínica",
            "Nombre_Contacto": "Doctor",
            "CTA_Link": "https://cal.com/negocios-partner-tech/requerimientos-software-desarrollo",
            "Campana": "produccion_ccl_v1",
            "Nombre_Remitente": "Franco Guerrero",
            "Cargo_Remitente": "Director Comercial",
            "Email_Remitente": "fguerrero@partnertech.pe",
            "Email_Destinatario": DEST_EMAIL,
            "Email_Hash": hashlib.md5(DEST_EMAIL.encode()).hexdigest()
        }
    },
    {
        "name": "Base Stitch B (Final - Firma Alineada)",
        "file": "templates/base/base_diseno_b.html",
        "vars": {
            "Titulo_Pagina": "Soberanía Tecnológica CCL",
            "Asunto_Override": "Optimización Operativa para Policlínicos Asociados",
            "Nombre_Contacto": "Doctor",
            "CTA_Link": "https://partnertech.pe",
            "Campana": "produccion_ccl_v1",
            "Nombre_Remitente": "Franco Guerrero",
            "Cargo_Remitente": "Director Comercial",
            "Email_Remitente": "fguerrero@partnertech.pe",
            "Email_Destinatario": DEST_EMAIL,
            "Email_Hash": hashlib.md5(DEST_EMAIL.encode()).hexdigest()
        }
    }
]

def send_email(template_config):
    try:
        with open(template_config["file"], "r", encoding="utf-8") as f:
            html = f.read()
        
        for key, val in template_config["vars"].items():
            html = html.replace(f"{{{{{key}}}}}", str(val))

        msg = MIMEMultipart("related")
        asunto_base = template_config["vars"].get("Asunto_Override", f"Verificación: {template_config['name']}")
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg["Subject"] = f"{asunto_base} [{timestamp}]"
        msg["From"] = SENDER_EMAIL
        msg["To"] = DEST_EMAIL
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
            ("assets/Logo_ver3.png", "logo_oficial"),
            ("assets/Logo_ver3.png", "Logo_Color"), 
            ("assets/Logo_y_texto_Partner_Tech.png", "Logo_y_texto_Partner_Tech"),
            ("assets/Logo_y_texto_Partner_Tech.png", "Logo_Color"), # Fallback
            ("assets/icons/custom/agenda_red.png", "minimalist_agenda_red"),
            ("assets/icons/custom/history_green.png", "minimalist_history_green"),
            ("assets/icons/custom/agenda_navy.png", "minimalist_agenda_navy"),
            ("assets/icons/custom/history_navy.png", "minimalist_history_navy"),
            ("assets/icons/custom/finance_navy.png", "minimalist_finance_navy"),
            ("assets/icons/custom/whatsapp_white.png", "whatsapp_blanco"),
            ("assets/icons/icomoon/115-users.png", "minimalist_meeting")
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
            server.sendmail(SENDER_EMAIL, [DEST_EMAIL], msg.as_string())
        
        print(f"✅ Enviado: {template_config['name']}")
    except Exception as e:
        print(f"❌ Error en {template_config['name']}: {e}")

if __name__ == "__main__":
    print(f"🚀 Enviando validación final a {DEST_EMAIL}...")
    for t in TEMPLATES:
        send_email(t)
