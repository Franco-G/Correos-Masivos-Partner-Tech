import pandas as pd
import smtplib
import ssl
import time
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
from tkinterweb import HtmlFrame

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
        self.root.title("Partner Tech | Gestor de Envío Masivo")
        self.root.geometry("1100x700")
        
        # Configurar Estilos
        self.setup_styles()
        self.root.configure(bg="#f4f6f9")

        # Variables de control
        self.plantilla_var = tk.StringVar()
        self.espera_var = tk.IntVar(value=65)
        self.contador_var = tk.StringVar(value="Cargando destinatarios...")
        self.enviando = False
        
        # Perfiles de Envío
        self.perfiles = {
            "Franco Guerrero": {
                "email": "fguerrero@partnertech.pe",
                "pass": "Franco001",
                "cargo": "Sub-Gerente Comercial"
            },
            "Alexandra Cardozo": {
                "email": "acardozo@partnertech.pe",
                "pass": "acardozo001",
                "cargo": "Gerente Comercial"
            }
        }
        
        # Variables de Remitente (Inicializar con el primero)
        self.perfil_seleccionado = tk.StringVar(value="Franco Guerrero")
        self.nombre_remitente_var = tk.StringVar(value="Franco Guerrero")
        self.cargo_remitente_var = tk.StringVar(value=self.perfiles["Franco Guerrero"]["cargo"])
        self.email_remitente_var = tk.StringVar(value=self.perfiles["Franco Guerrero"]["email"])
        self.pass_remitente_var = tk.StringVar(value=self.perfiles["Franco Guerrero"]["pass"])
        self.asunto_var = tk.StringVar()

        # --- UI LAYOUT ---
        header_frame = tk.Frame(root, bg="#0021a4", height=60)
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="PARTNER TECH", style="Header.TLabel").pack(pady=15)
        
        # Contenedor Horizontal (2 Columnas)
        container = ttk.Frame(root, padding=10)
        container.pack(fill="both", expand=True)
        
        # COLUMNA IZQUIERDA: Configuración y Logs
        left_col = ttk.Frame(container, width=400)
        left_col.pack(side="left", fill="both", padx=(0, 10))
        left_col.pack_propagate(False)

        # Configuración
        frame_config = ttk.LabelFrame(left_col, text="⚙️ Configuración del Envío", padding=15)
        frame_config.pack(fill="x", pady=(0, 10))

        # --- SECCIÓN REMITENTE ---
        frame_remitente = ttk.LabelFrame(frame_config, text="👤 Seleccionar Remitente", padding=10)
        frame_remitente.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        self.combo_perfil = ttk.Combobox(frame_remitente, textvariable=self.perfil_seleccionado, values=list(self.perfiles.keys()), state="readonly", width=35)
        self.combo_perfil.pack(fill="x", pady=5)
        self.combo_perfil.bind("<<ComboboxSelected>>", self.cargar_perfil)
        
        # Etiquetas informativas (solo lectura)
        self.lbl_info_remitente = ttk.Label(frame_remitente, text=f"{self.email_remitente_var.get()} | {self.cargo_remitente_var.get()}", font=("Segoe UI", 8), foreground="#666")
        self.lbl_info_remitente.pack(fill="x")

        # --- SECCIÓN ENVÍO ---
        ttk.Label(frame_config, text="Plantilla:", style="Bold.TLabel").grid(row=1, column=0, sticky="w")
        self.combo_plantillas = ttk.Combobox(frame_config, textvariable=self.plantilla_var, state="readonly", width=35)
        self.combo_plantillas.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.combo_plantillas.bind("<<ComboboxSelected>>", self.actualizar_preview)

        ttk.Label(frame_config, text="Asunto:", style="Bold.TLabel").grid(row=2, column=0, sticky="w")
        opciones_asunto = [
            "{{Nombre_Remitente}}: ¿Tu software actual te limita?",
            "Optimiza tus procesos - {{Nombre_Remitente}} (Partner Tech)",
            "{{Nombre_Remitente}}: Una pregunta breve sobre tu operación",
            "Propuesta de desarrollo a medida de {{Nombre_Remitente}}",
            "Hola {{Nombre_Contacto}}, soy {{Nombre_Remitente}} de Partner Tech"
        ]
        self.combo_asunto = ttk.Combobox(frame_config, textvariable=self.asunto_var, values=opciones_asunto, width=35)
        self.combo_asunto.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.combo_asunto.current(0)

        ttk.Label(frame_config, text="Destinatarios:", style="Bold.TLabel").grid(row=3, column=0, sticky="w")
        ttk.Label(frame_config, textvariable=self.contador_var).grid(row=3, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(frame_config, text="Espera (seg):", style="Bold.TLabel").grid(row=4, column=0, sticky="w")
        self.scale_espera = tk.Scale(frame_config, from_=0, to=90, orient="horizontal", variable=self.espera_var, 
                                     bg="#f4f6f9", highlightthickness=0, troughcolor="#e2e8f0", activebackground="#1e53dd")
        self.scale_espera.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.btn_iniciar = ttk.Button(frame_config, text="🚀 INICIAR ENVÍO", command=self.iniciar_envio_thread, style="Action.TButton")
        self.btn_iniciar.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky="ew")

        # Logs
        frame_logs = ttk.LabelFrame(left_col, text="📝 Registro de Actividad", padding=10)
        frame_logs.pack(fill="both", expand=True)

        self.txt_log = scrolledtext.ScrolledText(frame_logs, state='disabled', height=10, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4")
        self.txt_log.pack(fill="both", expand=True)

        # COLUMNA DERECHA: Visor Preview Real
        right_col = ttk.LabelFrame(container, text="👁️ Vista Previa del Correo", padding=10)
        right_col.pack(side="right", fill="both", expand=True)

        self.visor_html = HtmlFrame(right_col, messages_enabled=False)
        self.visor_html.pack(fill="both", expand=True)

        # Barra de estado
        self.status_var = tk.StringVar(value="Listo.")
        self.status_bar = tk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w", bg="#001556", fg="white", padx=10)
        self.status_bar.pack(side="bottom", fill="x")

        # Inicialización
        self.cargar_plantillas()
        self.contar_destinatarios()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        COLOR_AZUL_OSCURO = "#0021a4"
        COLOR_AZUL_MEDIO = "#243a92"
        COLOR_AZUL_ELECTRICO = "#1e53dd"
        COLOR_BLANCO = "#ffffff"
        
        style.configure(".", background="#f4f6f9", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f4f6f9")
        style.configure("TLabelframe", background="#f4f6f9", bordercolor=COLOR_AZUL_MEDIO)
        style.configure("TLabelframe.Label", background="#f4f6f9", foreground=COLOR_AZUL_OSCURO, font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", background="#f4f6f9", foreground="#333333")
        style.configure("Header.TLabel", background=COLOR_AZUL_OSCURO, foreground=COLOR_BLANCO, font=("Orbitron", 18, "bold"))
        style.configure("Bold.TLabel", font=("Segoe UI", 10, "bold"), foreground=COLOR_AZUL_OSCURO)
        
        style.configure("Action.TButton", background=COLOR_AZUL_ELECTRICO, foreground=COLOR_BLANCO, font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map("Action.TButton", background=[('active', COLOR_AZUL_MEDIO), ('disabled', '#cccccc')])

    def log_msg(self, mensaje, nivel="INFO"):
        prefix = f"[{nivel}] " if nivel != "INFO" else ""
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, f"{prefix}{mensaje}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state='disabled')
        getattr(logging, nivel.lower())(mensaje)

    def cargar_plantillas(self):
        archivos = glob.glob("*.html")
        if archivos:
            self.combo_plantillas['values'] = archivos
            self.combo_plantillas.current(0)
            self.actualizar_preview()
        else:
            self.combo_plantillas['values'] = ["No se encontraron HTMLs"]
            self.btn_iniciar.config(state="disabled")

    def cargar_perfil(self, event=None):
        nombre = self.perfil_seleccionado.get()
        if nombre in self.perfiles:
            datos = self.perfiles[nombre]
            self.nombre_remitente_var.set(nombre)
            self.email_remitente_var.set(datos["email"])
            self.pass_remitente_var.set(datos["pass"])
            self.cargo_remitente_var.set(datos["cargo"])
            
            # Actualizar label info
            self.lbl_info_remitente.config(text=f"{datos['email']} | {datos['cargo']}")
            self.actualizar_preview()

    def contar_destinatarios(self):
        try:
            if os.path.exists(archivo_excel):
                df = pd.read_excel(archivo_excel)
                count = len(df)
                self.contador_var.set(f"{count} contactos detectados")
                return count
            else:
                self.contador_var.set("Excel no encontrado")
                return 0
        except Exception as e:
            self.contador_var.set("Error al leer Excel")
            return 0

    def actualizar_preview(self, event=None):
        archivo = self.plantilla_var.get()
        if not archivo or not os.path.exists(archivo): return
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Cargar HTML en el visor real y reemplazar placeholders con datos de ejemplo del remitente
            preview_content = content.replace('{{Nombre_Remitente}}', self.nombre_remitente_var.get())\
                                     .replace('{{Email_Remitente}}', self.email_remitente_var.get())\
                                     .replace('{{Cargo_Remitente}}', self.cargo_remitente_var.get())\
                                     .replace('{{Nombre_Contacto}}', "[Nombre Cliente]")\
                                     .replace('{{Email_Destinatario}}', "[Email Cliente]")
            
            self.visor_html.load_html(preview_content)
        except Exception as e:
            self.log_msg(f"Error en preview: {e}", "ERROR")

    def verificar_formato(self, email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except: return False

    def enviar_correo(self, nombre, email_destinatario, archivo_html):
        try:
            with open(archivo_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Datos del Remitente desde UI
            remitente_nombre = self.nombre_remitente_var.get()
            remitente_email = self.email_remitente_var.get()
            remitente_pass = self.pass_remitente_var.get()
            remitente_cargo = self.cargo_remitente_var.get()
            asunto_template = self.asunto_var.get()

            # Reemplazos en HTML
            html_content = html_content.replace('{{Nombre_Contacto}}', nombre)\
                                       .replace('{{Email_Destinatario}}', email_destinatario)\
                                       .replace('{{Nombre_Remitente}}', remitente_nombre)\
                                       .replace('{{Email_Remitente}}', remitente_email)\
                                       .replace('{{Cargo_Remitente}}', remitente_cargo)
            
            message = MIMEMultipart("related")
            message["Subject"] = asunto_template.replace('{{Nombre_Contacto}}', nombre)\
                                                .replace('{{Nombre_Remitente}}', remitente_nombre)
            message["From"] = remitente_email
            message["To"] = email_destinatario
            message["Date"] = formatdate(localtime=True)
            message["Message-ID"] = make_msgid(domain="partnertech.pe")
            message["List-Unsubscribe"] = "<mailto:negocios@partnertech.pe?subject=unsubscribe>"
            
            msg_alternative = MIMEMultipart("alternative")
            message.attach(msg_alternative)
            
            text_plain = f"Hola {nombre},\n\nGracias por tu interés en Partner Tech.\nDesarrollamos software a medida según sus necesidades.\n\nAtentamente,\n{remitente_nombre}"
            msg_alternative.attach(MIMEText(text_plain, "plain"))
            msg_alternative.attach(MIMEText(html_content, "html"))
            
            try:
                with open('Logo_blanco_ver1.png', 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<Logo_ver1>')
                    message.attach(img)
            except: pass
            
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(remitente_email, remitente_pass)
                server.sendmail(remitente_email, email_destinatario, message.as_string())
            return True
        except Exception as e:
            self.log_msg(f"Error con {email_destinatario}: {e}", "ERROR")
            return False

    def iniciar_envio_thread(self):
        num_correos = self.contar_destinatarios()
        espera_actual = self.espera_var.get()

        if num_correos > 100 and espera_actual < 60:
            messagebox.showwarning("Seguridad Anti-Spam", 
                                   f"Has seleccionado {num_correos} destinatarios (>100).\nPor seguridad, el tiempo de espera debe ser al menos 60 segundos.\n\nSe ha ajustado automáticamente.")
            self.espera_var.set(60)
            return

        self.btn_iniciar.config(state="disabled")
        self.enviando = True
        threading.Thread(target=self.proceso_envio, daemon=True).start()

    def proceso_envio(self):
        archivo_html = self.plantilla_var.get()
        log_csv = 'registro_envios.csv'
        espera = self.espera_var.get()
        
        try:
            self.log_msg("--- INICIANDO ENVÍO MASIVO ---")
            df = pd.read_excel(archivo_excel)
            if not os.path.exists(log_csv):
                with open(log_csv, 'w', encoding='utf-8') as f: f.write("Nombre,Correo,Plantilla,Fecha,Estado\n")
            
            total = len(df)
            for idx, row in df.iterrows():
                if not self.enviando: break
                nombre, correo = str(row['nombre']).strip(), str(row['correo']).strip()
                self.status_var.set(f"Enviando {idx+1}/{total}: {correo}")
                
                if not self.verificar_formato(correo):
                    self.log_msg(f"Omitido (Formato): {correo}", "WARNING")
                    continue
                
                exito = self.enviar_correo(nombre, correo, archivo_html)
                estado = "Enviado" if exito else "Fallido"
                
                with open(log_csv, 'a', encoding='utf-8') as f:
                    f.write(f'"{nombre}","{correo}","{archivo_html}","{time.strftime("%Y-%m-%d %H:%M:%S")}","{estado}"\n')
                
                # Loguear siempre el resultado
                resultado_msg = f"OK: {correo}" if exito else f"FALLÓ: {correo}"
                self.log_msg(resultado_msg)
                
                if idx + 1 < total:
                    self.log_msg(f"Esperando {espera}s...")
                    time.sleep(espera)
            
            self.log_msg("--- PROCESO FINALIZADO ---")
            messagebox.showinfo("Completado", "El envío masivo ha terminado.")
        except Exception as e:
            self.log_msg(f"Error crítico: {e}", "CRITICAL")
        finally:
            self.enviando = False
            self.btn_iniciar.config(state="normal")
            self.status_var.set("Finalizado")

if __name__ == "__main__":
    root = tk.Tk()
    app = CorreoApp(root)
    root.mainloop()
