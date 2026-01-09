import pandas as pd
import smtplib
import ssl
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate, make_msgid
import logging
from email_validator import validate_email, EmailNotValidError

# --- CONFIGURACIÓN LOGGING ---
logging.basicConfig(
    filename='registro_envios.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- CONFIGURACIÓN ---
# Ajusta el nombre de tu archivo Excel aquí
archivo_excel = 'Correos.xlsx' 
archivo_html = 'correo_brochure.html' # Nombre de la plantilla HTML a utilizar

# --- CONFIGURACIÓN CORREO ---
smtp_server = "mail.partnertech.pe"
smtp_port = 465
sender_email = "fguerrero@partnertech.pe"
# IMPORTANTE: Coloca aquí la contraseña real de tu correo
password_email = "Franco001"

def verificar_formato(email):
    try:
        # check_deliverability=True verifica que el dominio tenga registros MX (DNS) válidos
        validate_email(email, check_deliverability=True)
        return True
    except EmailNotValidError:
        return False

def enviar_correo(nombre, email_destinatario):


    try:
        print(f"Preparando envío de correo a {email_destinatario}...")
        
        with open(archivo_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Construir el nombre de contacto completo
        nombre_completo_contacto = nombre
            
        html_content = html_content.replace('{{Nombre_Contacto}}', nombre_completo_contacto)
        # La línea para Nombre_Empresa se eliminará
        html_content = html_content.replace('{{Email_Destinatario}}', email_destinatario)
        
        message = MIMEMultipart("related")
        message["Subject"] = f"{nombre}, ¿tu software actual te limita? Hablemos." # Asunto modificado
        message["From"] = sender_email
        message["To"] = email_destinatario
        message["Date"] = formatdate(localtime=True)
        message["Message-ID"] = make_msgid(domain="partnertech.pe")
        message["List-Unsubscribe"] = "<mailto:negocios@partnertech.pe?subject=unsubscribe>"
        
        msg_alternative = MIMEMultipart("alternative")
        message.attach(msg_alternative)
        
        # Versión en texto plano para los filtros de spam
        # NOTA: Si cambias el archivo HTML, recuerda actualizar también este texto para que coincida con el mensaje.
        text_content = f"""
Hola {nombre_completo_contacto},

Gracias por tu interés en Partner Tech.

Sabemos que a medida que una empresa crece, el software genérico empieza a quedar chico. Nosotros construimos el software exactamente como su operación lo necesita.

Si desea agendar una reunión, visite: https://cal.com/negocios-partner-tech/requerimientos-software-desarrollo

Atentamente,
Franco Guerrero
Partner Tech
"""
        msg_alternative.attach(MIMEText(text_content, "plain"))
        msg_alternative.attach(MIMEText(html_content, "html"))
        
        def adjuntar_imagen(nombre_archivo, cid):
            try:
                with open(nombre_archivo, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', f'<{cid}>')
                    message.attach(img)
            except FileNotFoundError:
                print(f"Advertencia: No se encontró la imagen {nombre_archivo}")

        adjuntar_imagen('Logo_blanco_ver1.png', 'Logo_ver1')
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, password_email)
            # sendmail devuelve un diccionario si hay fallos inmediatos
            errores = server.sendmail(sender_email, email_destinatario, message.as_string())
            
        if errores:
            print(f"Advertencia: El servidor rechazó el envío a {email_destinatario}: {errores}")
            logging.error(f"RECHAZADO POR SERVIDOR: {email_destinatario} - {errores}")
            return False

        print(f"¡Correo enviado exitosamente a {email_destinatario}!")
        return True
        
    except Exception as e:
        print(f"Error al enviar el correo a {email_destinatario}: {e}")
        logging.error(f"FALLO: {email_destinatario} - Error: {e}")
        return False

def main():
    try:
        logging.info("--- Inicio del proceso de envío masivo ---")
        print(f"Leyendo archivo Excel: {archivo_excel}...")
        df = pd.read_excel(archivo_excel)
        
        log_enviados_file = 'registro_envios.csv'
        
        for index, row in df.iterrows():
            nombre = row['nombre']
            email_destinatario = row['correo']
            
            # Verificar si el email es un valor válido (no NaN y es string)
            if pd.isna(email_destinatario) or not isinstance(email_destinatario, str):
                print(f"Correo omitido por valor inválido en Excel: {email_destinatario}")
                logging.warning(f"OMITIDO: {email_destinatario} - Valor inválido en Excel")
                continue

            if not verificar_formato(email_destinatario):
                print(f"Correo omitido por formato inválido: {email_destinatario}")
                logging.warning(f"OMITIDO: {email_destinatario} - Formato inválido")
                continue
            
            if enviar_correo(nombre, email_destinatario):
                try:
                    with open(log_enviados_file, 'a', encoding='utf-8') as f:
                        fecha_actual = time.strftime("%Y-%m-%d")
                        f.write(f"{nombre},{email_destinatario},{archivo_html},{fecha_actual}\n")
                except Exception as e:
                    print(f"Error al escribir en el log de envíos exitosos: {e}")
                    logging.error(f"No se pudo escribir en {log_enviados_file}: {e}")
            
            time.sleep(random.randint(60, 65)) # Espera entre 60 y 65 segundos para evitar filtros de spam
            
        print("¡Proceso de envío de correos completado!")
        logging.info("--- Fin del proceso de envío masivo ---")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo Excel '{archivo_excel}'. Asegúrate de que el archivo existe en la misma carpeta que el script.")
        logging.critical(f"No se encontró el archivo Excel: {archivo_excel}")
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo Excel: {e}")
        logging.critical(f"Error crítico en el proceso: {e}")

if __name__ == "__main__":
    main()
