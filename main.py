import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# --- CONFIGURACIÓN ---
# Ajusta el nombre de tu archivo Excel aquí
archivo_excel = 'Correos.xlsx' 

# --- CONFIGURACIÓN CORREO ---
smtp_server = "mail.partnertech.pe"
smtp_port = 465
sender_email = "fguerrero@partnertech.pe"
# IMPORTANTE: Coloca aquí la contraseña real de tu correo
password_email = "Franco001"

def enviar_correo(nombre, tratamiento, email_destinatario):


    try:
        print(f"Preparando envío de correo a {email_destinatario}...")
        
        with open('template.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Construir el nombre de contacto completo
        nombre_completo_contacto = f"{tratamiento} {nombre}" if pd.notna(tratamiento) and tratamiento.strip() else nombre
            
        html_content = html_content.replace('{{Nombre_Contacto}}', nombre_completo_contacto)
        # La línea para Nombre_Empresa se eliminará
        html_content = html_content.replace('{{Email_Destinatario}}', email_destinatario)
        
        message = MIMEMultipart("related")
        message["Subject"] = f"Invitación de Partner Tech" # Asunto modificado
        message["From"] = sender_email
        message["To"] = email_destinatario
        
        msg_alternative = MIMEMultipart("alternative")
        message.attach(msg_alternative)
        
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
            server.sendmail(sender_email, email_destinatario, message.as_string())
            
        print(f"¡Correo enviado exitosamente a {email_destinatario}!")
        return True
        
    except Exception as e:
        print(f"Error al enviar el correo a {email_destinatario}: {e}")
        return False

def main():
    try:
        print(f"Leyendo archivo Excel: {archivo_excel}...")
        df = pd.read_excel(archivo_excel)
        
        for index, row in df.iterrows():
            # Asumimos que las columnas se llaman 'correo', 'nombre', 'tratamiento'
            nombre = row['nombre']
            tratamiento = row['tratamiento']
            email_destinatario = row['correo']
            # La columna 'nombre_empresa' ya no se lee
            
            enviar_correo(nombre, tratamiento, email_destinatario) # Se eliminó nombre_empresa
            
        print("¡Proceso de envío de correos completado!")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo Excel '{archivo_excel}'. Asegúrate de que el archivo existe en la misma carpeta que el script.")
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo Excel: {e}")

if __name__ == "__main__":
    main()
