import pandas as pd
from sqlalchemy import create_engine, MetaData, text
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# --- CONFIGURACIÓN ---
# Ajusta el nombre de tu archivo Excel aquí
archivo_excel = 'mi_archivo.xlsx' 
# Nombre que tendrá la tabla en PostgreSQL
nombre_tabla_destino = 'tabla_importada' 

# Datos de conexión basados en tu input
usuario = 'postgres'
contrasena = 'admin'
host = 'localhost'
puerto = '5432'
base_de_datos = 'directorioccl'

# Crear la cadena de conexión completa
cadena_conexion = f'postgresql+psycopg2://{usuario}:{contrasena}@{host}:{puerto}/{base_de_datos}'

# --- CONFIGURACIÓN CORREO ---
smtp_server = "mail.partnertech.pe"
smtp_port = 465
sender_email = "fguerrero@partnertech.pe"
# IMPORTANTE: Coloca aquí la contraseña real de tu correo
password_email = "Franco001"
receiver_email = "negocios@partnertech.pe"

def enviar_correo_ejemplo():
    try:
        print(f"Preparando envío de correo a {receiver_email}...")
        
        # Leer el archivo template.html
        with open('template.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Personalizar el contenido (Reemplazamos las variables del nuevo template)
        html_content = html_content.replace('{{Contacto_Nombre}}', 'Negocios PartnerTech')
        html_content = html_content.replace('{{Nombre_Empresa}}', 'Empresa de Prueba S.A.C.')
        
        # Crear el objeto mensaje
        # Usamos 'related' para permitir imágenes incrustadas (CIDs)
        message = MIMEMultipart("related")
        message["Subject"] = "Correo de prueba - Ejemplo Python"
        message["From"] = sender_email
        message["To"] = receiver_email
        
        # Parte alternativa para el contenido HTML
        msg_alternative = MIMEMultipart("alternative")
        message.attach(msg_alternative)
        
        # Adjuntar el HTML a la parte alternativa
        msg_alternative.attach(MIMEText(html_content, "html"))
        
        # Función auxiliar para adjuntar imágenes
        def adjuntar_imagen(nombre_archivo, cid):
            try:
                with open(nombre_archivo, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', f'<{cid}>')
                    message.attach(img)
            except FileNotFoundError:
                print(f"Advertencia: No se encontró la imagen {nombre_archivo}")

        # Adjuntar los logos (Asegúrate de que los archivos .png existan en la carpeta)
        adjuntar_imagen('Logo_blanco_ver1.png', 'Logo_blanco_ver1')
        adjuntar_imagen('Logo_ver1.png', 'Logo_ver1')
        
        # Conexión segura SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, message.as_string())
            
        print("¡Correo enviado exitosamente!")
        
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def main():
    # Ejecutar envío de correo de ejemplo
    enviar_correo_ejemplo()
    
    # Detenemos aquí para no ejecutar la parte de base de datos en esta prueba
    return

    try:
        # Crear el motor de conexión
        engine = create_engine(cadena_conexion)
        
        # 1. ELIMINAR TODAS LAS TABLAS (Limpieza de la BD)
        # Usamos MetaData para reflejar y borrar todo el esquema público
        print(f"Conectando a {base_de_datos} para limpiar tablas...")
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        if metadata.tables:
            print(f"Se encontraron {len(metadata.tables)} tablas. Eliminando...")
            metadata.drop_all(bind=engine)
            print("Todas las tablas han sido eliminadas exitosamente.")
        else:
            print("La base de datos ya estaba vacía.")

        # 2. SUBIR LA TABLA DE EXCEL
        print(f"Leyendo archivo Excel: {archivo_excel}...")
        # Lee el archivo Excel. Si tiene varias hojas, lee la primera por defecto.
        df = pd.read_excel(archivo_excel)
        
        print(f"Subiendo {len(df)} filas a la tabla '{nombre_tabla_destino}'...")
        
        # 'if_exists="replace"' crea la tabla, o la reemplaza si ya existe.
        # 'index=False' evita que se suba el índice numérico de pandas como una columna extra.
        df.to_sql(name=nombre_tabla_destino, con=engine, if_exists='replace', index=False)
        
        print("¡Proceso completado exitosamente!")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
