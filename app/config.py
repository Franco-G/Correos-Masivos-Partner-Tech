import os
import logging
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    SMTP_SERVER = os.getenv("SMTP_SERVER", "mail.partnertech.pe")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
    
    # Credenciales por defecto (Serán sobreescritas por perfiles si es necesario)
    DEFAULT_SENDER_EMAIL = os.getenv("SENDER_EMAIL", "fguerrero@partnertech.pe")
    DEFAULT_SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD", "Franco001")
    
    # Rutas de recursos
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGO_PATH = os.path.join(BASE_DIR, 'Logo_blanco_ver1.png')
    
    @staticmethod
    def validate():
        """Valida configuraciones críticas (Fail-fast)"""
        if not Config.DEFAULT_SENDER_PASSWORD:
            logging.warning("EMAIL_PASSWORD no detectado en el entorno.")
        return True
