import pandas as pd
import smtplib
import ssl
import time
import random
import glob
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
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
archivo_excel = 'Correos.xlsx'
smtp_server = "mail.partnertech.pe"
smtp_port = 465
sender_email = "fguerrero@partnertech.pe"
password_email = "Franco001"

class CorreoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Envío de Correos Masivos - Partner Tech")
        self.root.geometry("700x550")
        
        # Configurar Estilos
        self.setup_styles()
        
        self.root.configure(bg="#f4f6f9") # Fondo general gris muy claro

        # Variables de control
        self.plantilla_var = tk.StringVar()
        self.enviando = False

        # --- UI LAYOUT ---
        
        # Header Logotipo
        header_frame = tk.Frame(root, bg="#0021a4", height=60)
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="PARTNER TECH", style="Header.TLabel").pack(pady=15)
        
        # Frame Principal
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Sección Configuración
        frame_config = ttk.LabelFrame(main_frame, text="Configuración del Envío", padding=15)
        frame_config.pack(fill="x", pady=10)

        ttk.Label(frame_config, text="Seleccionar Plantilla HTML:", style="Bold.TLabel").grid(row=0, column=0, sticky="w", padx=5)
        
        self.combo_plantillas = ttk.Combobox(frame_config, textvariable=self.plantilla_var, state="readonly", width=50)
        self.combo_plantillas.grid(row=0, column=1, padx=10, pady=5)
        self.cargar_plantillas()

        # Botón de Inicio
        self.btn_iniciar = ttk.Button(frame_config, text="COMENZAR ENVÍO MASIVO", command=self.iniciar_envio_thread, style="Action.TButton")
        self.btn_iniciar.grid(row=1, column=0, columnspan=2, pady=20)

        # Frame Logs
        frame_logs = ttk.LabelFrame(main_frame, text="Registro de Actividad", padding=10)
        frame_logs.pack(fill="both", expand=True, pady=10)

        self.txt_log = scrolledtext.ScrolledText(frame_logs, state='disabled', height=10, font=("Consolas", 9))
        self.txt_log.pack(fill="both", expand=True)

        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Listo para iniciar.")
        self.status_bar = tk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w", bg="#001556", fg="white", padx=10)
        self.status_bar.pack(side="bottom", fill="x")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # Base para mayor control de colores
        
        # Colores Partner Tech
        COLOR_AZUL_OSCURO = "#0021a4"
        COLOR_AZUL_MEDIO = "#243a92"
        COLOR_AZUL_ELECTRICO = "#1e53dd"
        COLOR_BLANCO = "#ffffff"
        
        # Configuración General
        style.configure(".", background="#f4f6f9", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f4f6f9")
        style.configure("TLabelframe", background="#f4f6f9", bordercolor=COLOR_AZUL_MEDIO)
        style.configure("TLabelframe.Label", background="#f4f6f9", foreground=COLOR_AZUL_OSCURO, font=("Segoe UI", 11, "bold"))
        
        # Etiquetas
        style.configure("TLabel", background="#f4f6f9", foreground="#333333")
        style.configure("Header.TLabel", background=COLOR_AZUL_OSCURO, foreground=COLOR_BLANCO, font=("Orbitron", 18, "bold"))
        style.configure("Bold.TLabel", font=("Segoe UI", 10, "bold"), foreground=COLOR_AZUL_OSCURO)
        
        # Botón Acción Principal
        style.configure("Action.TButton", 
                        background=COLOR_AZUL_ELECTRICO, 
                        foreground=COLOR_BLANCO, 
                        font=("Segoe UI", 11, "bold"),
                        borderwidth=0,
                        focuscolor="none")
        style.map("Action.TButton", 
                  background=[('active', COLOR_AZUL_MEDIO), ('disabled', '#cccccc')],
                  foreground=[('disabled', '#666666')])

    def log_msg(self, mensaje, nivel="INFO"):
        """Agrega mensaje al log visual y al archivo log."""
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, f"{mensaje}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state='disabled')
        
        # Logging al archivo
        if nivel == "INFO":
            logging.info(mensaje)
        elif nivel == "ERROR":
            logging.error(mensaje)
        elif nivel == "WARNING":
            logging.warning(mensaje)
        elif nivel == "CRITICAL":
            logging.critical(mensaje)

    def cargar_plantillas(self):
        """Busca archivos .html en el directorio actual."""
        archivos = glob.glob("*.html")
        if archivos:
            self.combo_plantillas['values'] = archivos
            self.combo_plantillas.current(0)
        else:
            self.combo_plantillas['values'] = ["No se encontraron archivos .html"]
            self.btn_iniciar.config(state="disabled")

    def verificar_formato(self, email):
        try:
            validate_email(email, check_deliverability=True)
            return True
        except EmailNotValidError:
            return False

    def enviar_correo(self, nombre, email_destinatario, archivo_html):
        try:
            self.log_msg(f"Preparando envío a {email_destinatario}...", "INFO")
            
            with open(archivo_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            nombre_completo_contacto = nombre
                
            html_content = html_content.replace('{{Nombre_Contacto}}', nombre_completo_contacto)
            html_content = html_content.replace('{{Email_Destinatario}}', email_destinatario)
            
            message = MIMEMultipart("related")
            message["Subject"] = f"{nombre}, ¿tu software actual te limita? Hablemos."
            message["From"] = sender_email
            message["To"] = email_destinatario
            message["Date"] = formatdate(localtime=True)
            message["Message-ID"] = make_msgid(domain="partnertech.pe")
            message["List-Unsubscribe"] = "<mailto:negocios@partnertech.pe?subject=unsubscribe>"
            
            msg_alternative = MIMEMultipart("alternative")
            message.attach(msg_alternative)
            
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
                    self.log_msg(f"Advertencia: No se encontró la imagen {nombre_archivo}", "WARNING")

            adjuntar_imagen('Logo_blanco_ver1.png', 'Logo_ver1')
            
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(sender_email, password_email)
                errores = server.sendmail(sender_email, email_destinatario, message.as_string())
                
            if errores:
                self.log_msg(f"Advertencia: Rechazado por servidor a {email_destinatario}: {errores}", "ERROR")
                return False

            self.log_msg(f"¡Correo enviado exitosamente a {email_destinatario}!", "INFO")
            return True
            
        except Exception as e:
            self.log_msg(f"Error enviando a {email_destinatario}: {e}", "ERROR")
            return False

    def iniciar_envio_thread(self):
        """Wrapper para ejecutar el proceso en un hilo separado."""
        if not self.combo_plantillas.get() or self.combo_plantillas.get() == "No se encontraron archivos .html":
            messagebox.showerror("Error", "Seleccione una plantilla válida.")
            return

        self.btn_iniciar.config(state="disabled")
        self.enviando = True
        hilo = threading.Thread(target=self.proceso_envio)
        hilo.start()

    def proceso_envio(self):
        archivo_html_seleccionado = self.plantilla_var.get()
        self.status_var.set("Proceso activo...")
        log_csv = 'registro_envios.csv'
        
        try:
            self.log_msg("--- Inicio del proceso de envío masivo ---", "INFO")
            
            if not os.path.exists(archivo_excel):
                error_msg = f"No se encontró el archivo obligatorio: {archivo_excel}"
                self.log_msg(error_msg, "CRITICAL")
                messagebox.showerror("Archivo No Encontrado", error_msg)
                return

            self.log_msg(f"Leyendo base de datos: {archivo_excel}...", "INFO")
            df = pd.read_excel(archivo_excel)
            
            # Verificar columnas necesarias
            if 'nombre' not in df.columns or 'correo' not in df.columns:
                raise ValueError("El Excel debe tener las columnas 'nombre' y 'correo'.")

            # Preparar CSV de registros si no existe
            if not os.path.exists(log_csv):
                with open(log_csv, 'w', encoding='utf-8') as f:
                    f.write("Nombre,Correo,Plantilla,Fecha,Estado\n")
            
            total = len(df)
            procesados = 0

            for index, row in df.iterrows():
                if not self.enviando: break # Cancelación manual si se implementara
                
                procesados += 1
                nombre = str(row['nombre']).strip()
                email_destinatario = str(row['correo']).strip()
                
                self.status_var.set(f"Procesando {procesados}/{total}: {email_destinatario}")
                
                if not email_destinatario or email_destinatario == "nan":
                    self.log_msg(f"[{procesados}] Omitido: Celda vacía en fila {index+2}", "WARNING")
                    continue

                if not self.verificar_formato(email_destinatario):
                    self.log_msg(f"[{procesados}] Omitido (Formato Inválido): {email_destinatario}", "WARNING")
                    continue
                
                exito = self.enviar_correo(nombre, email_destinatario, archivo_html_seleccionado)
                estado = "Enviado" if exito else "Fallido"
                
                # Registro en CSV
                try:
                    fecha_log = time.strftime("%Y-%m-%d %H:%M:%S")
                    with open(log_csv, 'a', encoding='utf-8') as f:
                        f.write(f'"{nombre}","{email_destinatario}","{archivo_html_seleccionado}","{fecha_log}","{estado}"\n')
                except Exception as e:
                    self.log_msg(f"Error escribiendo en CSV: {e}", "ERROR")
                
                if procesados < total:
                    espera = random.randint(60, 65)
                    self.log_msg(f"Esperando {espera}s para el siguiente envío...", "INFO")
                    time.sleep(espera)
                
            self.log_msg("--- Proceso completado exitosamente ---", "INFO")
            messagebox.showinfo("Fin del Proceso", f"Se han procesado {procesados} registros.\nConsulte {log_csv} para detalles.")

        except Exception as e:
            self.log_msg(f"Error crítico en el proceso: {e}", "CRITICAL")
            messagebox.showerror("Error Crítico", str(e))
        
        finally:
            self.enviando = False
            self.btn_iniciar.config(state="normal")
            self.status_var.set("Finalizado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CorreoApp(root)
    root.mainloop()
