import os
import smtplib
import ssl
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate, make_msgid

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
            "Titulo_Pagina": "Evolución Clínica | Partner Tech",
            "Nombre_Producto": "Clinic Mentor Pro",
            "Asunto_Override": "Diseño A: Evolución y Comparativa Médica",
            "Titulo_Principal": "Optimice su Gestión Médica Hoy",
            "Subtitulo": "De la administración manual a la soberanía tecnológica.",
            "Nombre_Contacto": "Franco",
            "Titulo_Problema": "Ineficiencia y Caos Administrativo",
            "Texto_Problema": "Agendas desordenadas, liquidaciones manuales que tardan días y pérdida de datos críticos del paciente.",
            "Titulo_Solucion": "Digitalización y Rentabilidad Real",
            "Texto_Solucion": "Agenda omnicanal, historia clínica digital segura y liquidaciones automáticas que transforman su clínica.",
            "CTA_Titulo": "¿Desea ver cómo funciona en vivo?",
            "CTA_Link": "https://cal.com/negocios-partner-tech/requerimientos-software-desarrollo",
            "Campana": "base_a_final_validation",
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
            "Titulo_Pagina": "Máxima Eficiencia Clínica",
            "Nombre_Producto": "Clinic Mentor Premium",
            "Asunto_Override": "Diseño B: Enfoque en Eficiencia y Rentabilidad",
            "Hero_Title": "Transforme la Salud de su Negocio",
            "Hero_Text": "El sistema que permite a los médicos enfocarse en pacientes, no en papeles.",
            "Problem_Title": "El Costo de Oportunidad Manual",
            "Problem_Text": "Cada minuto perdido buscando una historia o cuadrando una caja es rentabilidad perdida.",
            "Solution_Title": "Control Total de su Policlínico",
            "Solution_Text": "Visibilidad de métricas en tiempo real y un equipo administrativo mucho más productivo.",
            "CTA_Link": "https://partnertech.pe",
            "Campana": "base_b_final_validation",
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
        asunto = template_config["vars"].get("Asunto_Override", f"Verificación: {template_config['name']}")
        msg["Subject"] = asunto
        msg["From"] = SENDER_EMAIL
        msg["To"] = DEST_EMAIL
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="partnertech.pe")

        msg_alt = MIMEMultipart("alternative")
        msg.attach(msg_alt)
        msg_alt.attach(MIMEText(html, "html"))

        # Mapeo de activos (CIDs DEBEN COINCIDIR CON EL HTML)
        assets = [
            ("assets/Logo_blanco_ver3.png", "Logo_blanco_ver3"),
            ("assets/Logo_blanco_ver1.png", "Logo_ver1"), # Usado en Base B
            ("assets/Logo_y_texto_Partner_Tech.png", "Logo_y_texto_Partner_Tech"),
            ("assets/Logo_y_texto_Partner_Tech.png", "Logo_Color"), # Fallback
            ("assets/benefit_agenda.png", "benefit_agenda"),
            ("assets/benefit_historia.png", "benefit_historia"),
            ("assets/benefit_liquidacion.png", "benefit_liquidacion"),
            ("assets/benefit_reunion.png", "benefit_reunion")
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
