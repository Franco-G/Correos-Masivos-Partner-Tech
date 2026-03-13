import pandas as pd
import smtplib
import ssl
import time
import random
import glob
import os
import threading
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import scrolledtext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate, make_msgid
import logging
from email_validator import validate_email, EmailNotValidError
from tkinterweb import HtmlFrame
import base64
import io
import sqlite3
from datetime import datetime, timedelta



def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        # Assuming PNG for now, can be made dynamic if needed
        return f"data:image/png;base64,{encoded_string}"
    except Exception as e:
        logging.error(f"Error encoding image to base64: {e}")
        return ""

# --- CONFIGURACIÓN LOGGING ---
if not os.path.exists('data'):
    os.makedirs('data')
logging.basicConfig(
    filename=os.path.join('data', 'registro_envios.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- CONFIGURACIÓN ---
smtp_server = "mail.partnertech.pe"
smtp_port = 465
sender_email = "fguerrero@partnertech.pe"
password_email = "Franco001"

class CorreoApp:
    # Type hints for Pyre2
    root: tk.Tk
    db_path: str
    combo_perfil: ttk.Combobox
    lbl_info_remitente: ttk.Label
    combo_plantilla1: ttk.Combobox
    combo_plantilla2: ttk.Combobox
    combo_plantilla3: ttk.Combobox
    combo_asunto: ttk.Combobox
    btn_cargar: ttk.Button
    btn_iniciar: ttk.Button
    txt_log: scrolledtext.ScrolledText
    spin_dias: ttk.Spinbox
    lbl_stats: ttk.Label
    tree_destinatarios: ttk.Treeview
    ent_email_test: ttk.Entry
    canvas_test: tk.Canvas
    scroll_test: ttk.Scrollbar
    frame_checkboxes: ttk.Frame
    btn_enviar_prueba: ttk.Button
    
    plantilla1_var: tk.StringVar
    plantilla2_var: tk.StringVar
    plantilla3_var: tk.StringVar
    email_prueba_var: tk.StringVar
    plantillas_test_vars: dict[str, tk.BooleanVar]
    contador_var: tk.StringVar
    enviando: bool
    archivo_excel_seleccionado: str
    dias_espera_var: tk.IntVar
    
    perfiles: dict[str, dict[str, str]]
    perfil_seleccionado: tk.StringVar
    nombre_remitente_var: tk.StringVar
    cargo_remitente_var: tk.StringVar
    email_remitente_var: tk.StringVar
    pass_remitente_var: tk.StringVar
    asunto_var: tk.StringVar
    
    notebook: ttk.Notebook
    tab_envio: ttk.Frame
    tab_pruebas: ttk.Frame
    status_var: tk.StringVar
    status_bar: tk.Label

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Partner Tech | Gestor de Envío Masivo")
        self.root.state('zoomed')
        self.root.geometry("1100x700")
        
        # Variables de control
        self.plantilla1_var = tk.StringVar()
        self.plantilla2_var = tk.StringVar(value="Ninguna")
        self.plantilla3_var = tk.StringVar(value="Ninguna")
        self.email_prueba_var = tk.StringVar()
        self.plantillas_test_vars = {} 
        self.contador_var = tk.StringVar(value="Ningún archivo seleccionado")
        self.enviando = False
        self.archivo_excel_seleccionado = ""
        self.dias_espera_var = tk.IntVar(value=15)
        
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
                "cargo": "Chief Business Officer<br>Directora de Negocios"
            }
        }
        
        self.perfil_seleccionado = tk.StringVar(value="Alexandra Cardozo")
        self.nombre_remitente_var = tk.StringVar(value="Alexandra Cardozo")
        self.cargo_remitente_var = tk.StringVar(value=self.perfiles["Alexandra Cardozo"]["cargo"])
        self.email_remitente_var = tk.StringVar(value=self.perfiles["Alexandra Cardozo"]["email"])
        self.pass_remitente_var = tk.StringVar(value=self.perfiles["Alexandra Cardozo"]["pass"])
        self.asunto_var = tk.StringVar()

        # DB Setup
        self.db_path = ""
        self.setup_db()

        # Configurar Estilos
        self.setup_styles()
        self.root.configure(bg="#f4f6f9")

        # --- UI LAYOUT ---
        header_frame = tk.Frame(root, bg="#0021a4", height=60)
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="PARTNER TECH", style="Header.TLabel").pack(pady=15)
        
        # PESTAÑAS PRINCIPALES
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Panel de Envío
        self.tab_envio = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_envio, text=" 📨 Panel de Envío ")
        
        # Tab 2: Panel de Pruebas
        self.tab_pruebas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pruebas, text=" 🧪 Pruebas de Envío ")
        
        # Construcción de pestañas
        self.construir_tab_envio()
        self.construir_tab_pruebas()

        # Barra de estado
        self.status_var = tk.StringVar(value="Listo.")
        self.status_bar = tk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w", bg="#001556", fg="white", padx=10)
        self.status_bar.pack(side="bottom", fill="x")

        # Inicialización
        self.cargar_plantillas()
        self.contar_destinatarios()

    def setup_db(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        self.db_path = os.path.join('data', 'control_envios.db')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS envios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                correo TEXT,
                fecha_ultimo_envio TIMESTAMP,
                plantilla TEXT
            )
        ''')
        # Tabla de configuración
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY,
                valor TEXT
            )
        ''')
        # Cargar configuración de días
        cursor.execute("SELECT valor FROM configuracion WHERE clave = 'dias_espera'")
        res = cursor.fetchone()
        if res:
            self.dias_espera_var.set(int(res[0]))
        else:
            cursor.execute("INSERT INTO configuracion (clave, valor) VALUES ('dias_espera', '15')")
        conn.commit()
        conn.close()

    def guardar_config_dias(self):
        try:
            dias = self.dias_espera_var.get()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE configuracion SET valor = ? WHERE clave = 'dias_espera'", (str(dias),))
            conn.commit()
            conn.close()
            self.log_msg(f"Configuración guardada: {dias} días de espera.")
            messagebox.showinfo("Configuración", f"Se ha actualizado el periodo de espera a {dias} días.")
            self.actualizar_stats_db()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {e}")

    def es_elegible_envio(self, correo):
        try:
            dias_espera = self.dias_espera_var.get()
            if dias_espera <= 0:
                return True
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Buscar el último envío exitoso a este correo
            cursor.execute('''
                SELECT fecha_ultimo_envio FROM envios 
                WHERE correo = ? 
                ORDER BY fecha_ultimo_envio DESC LIMIT 1
            ''', (correo,))
            res = cursor.fetchone()
            conn.close()
            
            if not res:
                return True
                
            fecha_ultimo = datetime.strptime(res[0], "%Y-%m-%d %H:%M:%S")
            if datetime.now() > (fecha_ultimo + timedelta(days=dias_espera)):
                return True
            
            return False
        except Exception as e:
            self.log_msg(f"Error al verificar elegibilidad: {e}", "ERROR")
            return True # Por seguridad, permitimos el envío si falla la DB

    def registrar_envio_db(self, correo, plantilla):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO envios (correo, fecha_ultimo_envio, plantilla)
                VALUES (?, ?, ?)
            ''', (correo, fecha_actual, plantilla))
            conn.commit()
            conn.close()
        except Exception as e:
            self.log_msg(f"Error al registrar en DB: {e}", "ERROR")

    def construir_tab_pruebas(self):
        # Contenedor principal
        frame_main = ttk.Frame(self.tab_pruebas, padding=20)
        frame_main.pack(fill="both", expand=True)

        # Izquierda: Configuración de Prueba
        frame_test_config = ttk.LabelFrame(frame_main, text="⚙️ Configuración de Prueba", padding=15)
        frame_test_config.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(frame_test_config, text="Correo de Destino (Prueba):", style="Bold.TLabel").pack(anchor="w", pady=(0, 5))
        self.ent_email_test = ttk.Entry(frame_test_config, textvariable=self.email_prueba_var, font=("Segoe UI", 11))
        self.ent_email_test.pack(fill="x", pady=(0, 15))
        self.email_prueba_var.set(self.email_remitente_var.get()) # Por defecto el mismo remitente

        ttk.Label(frame_test_config, text="Seleccione Plantillas:", style="Bold.TLabel").pack(anchor="w", pady=(0, 5))
        
        # Botones de selección masiva
        frame_bulk = ttk.Frame(frame_test_config)
        frame_bulk.pack(fill="x", pady=(0, 5))
        ttk.Button(frame_bulk, text="☑ Seleccionar Todas", command=self.seleccionar_todas_pruebas).pack(side="left", padx=2)
        ttk.Button(frame_bulk, text="☐ Desmarcar Todas", command=self.desmarcar_todas_pruebas).pack(side="left", padx=2)

        # Área desplazable para checkboxes
        frame_scroll_container = ttk.Frame(frame_test_config, relief="flat", borderwidth=1)
        frame_scroll_container.pack(fill="both", expand=True)

        self.canvas_test = tk.Canvas(frame_scroll_container, highlightthickness=0, bg="#ffffff")
        self.scroll_test = ttk.Scrollbar(frame_scroll_container, orient="vertical", command=self.canvas_test.yview)
        self.frame_checkboxes = ttk.Frame(self.canvas_test)

        self.frame_checkboxes.bind("<Configure>", lambda e: self.canvas_test.configure(scrollregion=self.canvas_test.bbox("all")))
        self.canvas_test.create_window((0, 0), window=self.frame_checkboxes, anchor="nw")
        self.canvas_test.configure(yscrollcommand=self.scroll_test.set)

        self.canvas_test.pack(side="left", fill="both", expand=True)
        self.scroll_test.pack(side="right", fill="y")

        self.btn_enviar_prueba = ttk.Button(frame_test_config, text="📧 ENVIAR CORREOS DE PRUEBA", command=self.enviar_prueba_thread, style="Action.TButton")
        self.btn_enviar_prueba.pack(fill="x", pady=(15, 0))

        # Derecha: Info y Ayuda
        frame_test_info = ttk.LabelFrame(frame_main, text="ℹ️ Información", padding=15, width=350)
        frame_test_info.pack(side="right", fill="both")
        frame_test_info.pack_propagate(False) # Evitar que el frame colapse al contenido
        
        info_text = "Este módulo permite verificar cómo llegan los correos antes del envío masivo.\n\n" \
                    "1. Ingrese su correo personal.\n" \
                    "2. Marque las plantillas que desea probar.\n" \
                    "3. Se enviarán con un intervalo de 10-15s para simular un envío real y evitar bloqueos.\n\n" \
                    "Nota: Se utilizará el Remitente y Asunto configurados en el 'Panel de Envío'."
        
        ttk.Label(frame_test_info, text=info_text, wraplength=300, justify="left").pack(anchor="n")

    def seleccionar_todas_pruebas(self):
        for var in self.plantillas_test_vars.values():
            var.set(True)

    def desmarcar_todas_pruebas(self):
        for var in self.plantillas_test_vars.values():
            var.set(False)

    def enviar_prueba_thread(self):
        destinatario = self.email_prueba_var.get().strip()
        plantillas_seleccionadas = [name for name, var in self.plantillas_test_vars.items() if var.get()]
        
        if not destinatario or not self.verificar_formato(destinatario):
            messagebox.showerror("Error", "Ingrese un correo de destino válido.")
            return
        
        if not plantillas_seleccionadas:
            messagebox.showwarning("Atención", "Seleccione al menos una plantilla para probar.")
            return

        self.btn_enviar_prueba.config(state="disabled")
        threading.Thread(target=self.proceso_envio_prueba, args=(destinatario, plantillas_seleccionadas), daemon=True).start()

    def proceso_envio_prueba(self, destinatario, plantillas_seleccionadas):
        self.log_msg(f"--- INICIANDO PRUEBAS PARA: {destinatario} ---")
        total = len(plantillas_seleccionadas)
        
        for i, p_nombre in enumerate(plantillas_seleccionadas):
            self.status_var.set(f"Probando ({i+1}/{total}): {p_nombre}")
            exito = self.enviar_correo("Usuario Prueba", destinatario, p_nombre)
            resultado = "OK" if exito else "FALLÓ"
            self.log_msg(f"Prueba {p_nombre}: {resultado}")
            
            if i + 1 < total:
                espera = random.uniform(10, 15)
                self.log_msg(f"Esperando {espera:.2f}s para siguiente prueba...")
                time.sleep(espera)

        self.log_msg("--- PRUEBAS FINALIZADAS ---")
        self.status_var.set("Pruebas completadas")
        self.btn_enviar_prueba.config(state="normal")
        messagebox.showinfo("Pruebas", "Se han enviado los correos de prueba seleccionados.")

    def construir_tab_envio(self):
        # Contenedor principal con paneles redimensionables
        main_paned_window = ttk.PanedWindow(self.tab_envio, orient=tk.HORIZONTAL)
        main_paned_window.pack(fill="both", expand=True, padx=10, pady=10)

        # COLUMNA IZQUIERDA: Configuración y Logs
        left_col = ttk.Frame(main_paned_window, width=400)
        main_paned_window.add(left_col, weight=1)
        
        # Configuración
        frame_config = ttk.LabelFrame(left_col, text="⚙️ Configuración del Envío", padding=15)
        frame_config.pack(fill="x", pady=(0, 10))
        frame_config.grid_columnconfigure(1, weight=1)

        # --- SECCIÓN REMITENTE ---
        frame_remitente = ttk.LabelFrame(frame_config, text="👤 Seleccionar Remitente", padding=10)
        frame_remitente.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        self.combo_perfil = ttk.Combobox(frame_remitente, textvariable=self.perfil_seleccionado, values=list(self.perfiles.keys()), state="readonly")
        self.combo_perfil.pack(fill="x", pady=5)
        self.combo_perfil.bind("<<ComboboxSelected>>", self.cargar_perfil)
        
        self.lbl_info_remitente = ttk.Label(frame_remitente, text=f"{self.email_remitente_var.get()} | {self.cargo_remitente_var.get()}", font=("Segoe UI", 8), foreground="#666")
        self.lbl_info_remitente.pack(fill="x")

        # Plantilla 1 (Obligatoria)
        ttk.Label(frame_config, text="Plantilla 1 (Oblig):", style="Bold.TLabel").grid(row=1, column=0, sticky="w", pady=2)
        self.combo_plantilla1 = ttk.Combobox(frame_config, textvariable=self.plantilla1_var, state="readonly")
        self.combo_plantilla1.grid(row=1, column=1, padx=10, pady=2, sticky="ew")
        self.combo_plantilla1.bind("<<ComboboxSelected>>", self.actualizar_preview)

        # Plantilla 2 (Opcional)
        ttk.Label(frame_config, text="Plantilla 2 (Opc):", style="Bold.TLabel").grid(row=2, column=0, sticky="w", pady=2)
        self.combo_plantilla2 = ttk.Combobox(frame_config, textvariable=self.plantilla2_var, state="readonly")
        self.combo_plantilla2.grid(row=2, column=1, padx=10, pady=2, sticky="ew")

        # Plantilla 3 (Opcional)
        ttk.Label(frame_config, text="Plantilla 3 (Opc):", style="Bold.TLabel").grid(row=3, column=0, sticky="w", pady=2)
        self.combo_plantilla3 = ttk.Combobox(frame_config, textvariable=self.plantilla3_var, state="readonly")
        self.combo_plantilla3.grid(row=3, column=1, padx=10, pady=2, sticky="ew")

        ttk.Label(frame_config, text="Asunto:", style="Bold.TLabel").grid(row=4, column=0, sticky="w", pady=5)
        opciones_asunto = [
            "{{Nombre_Remitente}}: ¿Tu software actual te limita?",
            "Optimiza tus procesos - {{Nombre_Remitente}} (Partner Tech)",
            "{{Nombre_Remitente}}: Una pregunta breve sobre tu operación",
            "Propuesta de desarrollo a medida de {{Nombre_Remitente}}",
            "Hola {{Nombre_Contacto}}, soy {{Nombre_Remitente}} de Partner Tech"
        ]
        self.combo_asunto = ttk.Combobox(frame_config, textvariable=self.asunto_var, values=opciones_asunto)
        self.combo_asunto.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.combo_asunto.current(4) # "Hola {{Nombre_Contacto}}, soy {{Nombre_Remitente}} de Partner Tech"

        ttk.Label(frame_config, text="Archivo:", style="Bold.TLabel").grid(row=5, column=0, sticky="w", pady=5)
        self.btn_cargar = ttk.Button(frame_config, text="📁 Seleccionar Excel...", command=self.cargar_archivo_excel)
        self.btn_cargar.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame_config, text="Destinatarios:", style="Bold.TLabel").grid(row=6, column=0, sticky="w", pady=5)
        ttk.Label(frame_config, textvariable=self.contador_var).grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.btn_iniciar = ttk.Button(frame_config, text="🚀 INICIAR ENVÍO", command=self.iniciar_envio_thread, style="Action.TButton")
        self.btn_iniciar.grid(row=7, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        self.btn_iniciar.config(state="disabled")

        # Logs
        frame_logs = ttk.LabelFrame(left_col, text="📝 Registro de Actividad", padding=10)
        frame_logs.pack(fill="both", expand=True)

        self.txt_log = scrolledtext.ScrolledText(frame_logs, state='disabled', height=10, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4")
        self.txt_log.pack(fill="both", expand=True)

        # PANEL CENTRAL: Control de Envíos y Base de Datos (Reemplaza Vista Previa)
        center_col = ttk.LabelFrame(main_paned_window, text="🛡️ Control de Envíos (Anti-Duplicados)", padding=15)
        main_paned_window.add(center_col, weight=2)
        
        # Configuración de Días
        frame_db_config = ttk.Frame(center_col)
        frame_db_config.pack(fill="x", pady=(0, 20))
        
        ttk.Label(frame_db_config, text="Periodo de espera (días):", style="Bold.TLabel").pack(side="left", padx=5)
        self.spin_dias = ttk.Spinbox(frame_db_config, from_=0, to=365, textvariable=self.dias_espera_var, width=5)
        self.spin_dias.pack(side="left", padx=5)
        
        ttk.Button(frame_db_config, text="💾 Guardar Configuración", command=self.guardar_config_dias).pack(side="left", padx=10)
        
        # Información de Base de Datos
        ttk.Separator(center_col, orient="horizontal").pack(fill="x", pady=10)
        
        ttk.Label(center_col, text="Información del Sistema:", style="Bold.TLabel").pack(anchor="w", pady=5)
        
        info_db = "Esta funcionalidad utiliza una base de datos SQLite para asegurar que no se envíen correos repetidos a la misma persona en un corto periodo de tiempo.\n\n" \
                  "• Si el contacto ya recibió un correo hace menos de los días configurados, el sistema saltará ese envío.\n" \
                  "• Por defecto, el periodo es de 15 días.\n" \
                  "• Todos los envíos quedan registrados históricamente en `data/control_envios.db`."
        
        ttk.Label(center_col, text=info_db, wraplength=450, justify="left").pack(fill="x")
        
        # Estadísticas Rápidas
        self.lbl_stats = ttk.Label(center_col, text="\nResumen de Base de Datos: Cargando...", font=("Segoe UI", 9, "italic"))
        self.lbl_stats.pack(anchor="w", pady=20)
        self.actualizar_stats_db()

        # PANEL DERECHO: Lista de Destinatarios
        right_col = ttk.LabelFrame(main_paned_window, text="📋 Lista de Destinatarios", padding=10)
        main_paned_window.add(right_col, weight=1)

        # Treeview para mostrar la lista
        cols = ("Nombre", "Correo")
        self.tree_destinatarios = ttk.Treeview(right_col, columns=cols, show="headings", height=5)
        self.tree_destinatarios.heading("Nombre", text="Nombre")
        self.tree_destinatarios.heading("Correo", text="Correo")
        self.tree_destinatarios.column("Nombre", width=150)
        self.tree_destinatarios.column("Correo", width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(right_col, orient="vertical", command=self.tree_destinatarios.yview)
        self.tree_destinatarios.configure(yscrollcommand=scrollbar.set)
        
        self.tree_destinatarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def actualizar_stats_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM envios")
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT correo) FROM envios")
            contactos = cursor.fetchone()[0]
            conn.close()
            self.lbl_stats.config(text=f"\nResumen de Base de Datos:\n• Total de envíos registrados: {total}\n• Contactos únicos contactados: {contactos}")
        except:
            if hasattr(self, 'lbl_stats'):
                self.lbl_stats.config(text="\nResumen de Base de Datos: No disponible")

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
        nombres = []
        for root_dir, dirs, files in os.walk("templates"):
            for file in files:
                if file.endswith(".html"):
                    # Obtener ruta relativa para mostrar el "aplicativo/archivo"
                    rel_path = os.path.relpath(os.path.join(root_dir, file), "templates")
                    nombres.append(rel_path.replace("\\", "/"))

        if nombres:
            nombres = sorted(nombres)
            # Llenar Combos del Panel de Envío
            self.combo_plantilla1['values'] = nombres
            self.combo_plantilla2['values'] = ["Ninguna"] + nombres
            self.combo_plantilla3['values'] = ["Ninguna"] + nombres
            
            # Llenar Checkboxes del Panel de Pruebas
            for widget in self.frame_checkboxes.winfo_children():
                widget.destroy()
            
            self.plantillas_test_vars = {}
            for n in nombres:
                var = tk.BooleanVar()
                self.plantillas_test_vars[n] = var
                cb = ttk.Checkbutton(self.frame_checkboxes, text=n, variable=var)
                cb.pack(anchor="w", pady=2)

            # Intentar seleccionar el primero disponible
            if nombres:
                self.plantilla1_var.set(nombres[0])
            
            self.plantilla2_var.set("Ninguna")
            self.plantilla3_var.set("Ninguna")
            
            # self.actualizar_preview() # Eliminado ya que no hay visor HTML
        else:
            self.combo_plantilla1['values'] = ["No se encontraron HTMLs"]
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

    def cargar_archivo_excel(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo de correos",
            filetypes=(("Archivos de Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*"))
        )
        if not filepath:
            return

        self.archivo_excel_seleccionado = filepath
        self.contar_destinatarios()

    def contar_destinatarios(self):
        # Limpiar la lista de destinatarios antes de procesar
        self.actualizar_lista_destinatarios(None)

        if not self.archivo_excel_seleccionado:
            self.contador_var.set("Ningún archivo seleccionado")
            self.btn_iniciar.config(state="disabled")
            return 0
        
        try:
            if os.path.exists(self.archivo_excel_seleccionado):
                df = pd.read_excel(self.archivo_excel_seleccionado).fillna('')
                # Check for required columns
                if 'nombre' not in df.columns or 'correo' not in df.columns:
                    messagebox.showerror("Error de Archivo", "El archivo Excel debe contener las columnas 'nombre' y 'correo'.")
                    self.contador_var.set("Error: Faltan columnas")
                    self.btn_iniciar.config(state="disabled")
                    return 0
                
                count = len(df)
                self.contador_var.set(f"{count} contactos detectados")
                self.btn_iniciar.config(state="normal")
                self.log_msg(f"Archivo cargado: {os.path.basename(self.archivo_excel_seleccionado)}")
                
                # Actualizar la lista visual de destinatarios
                self.actualizar_lista_destinatarios(df)
                
                return count
            else:
                self.contador_var.set("Excel no encontrado")
                self.btn_iniciar.config(state="disabled")
                return 0
        except Exception as e:
            self.contador_var.set("Error al leer Excel")
            self.log_msg(f"Error al cargar Excel: {e}", "ERROR")
            self.btn_iniciar.config(state="disabled")
            return 0

    def actualizar_lista_destinatarios(self, df):
        # Limpiar Treeview
        for i in self.tree_destinatarios.get_children():
            self.tree_destinatarios.delete(i)

        # Llenar con nuevos datos si el dataframe es válido
        if df is not None and not df.empty:
            for index, row in df.iterrows():
                self.tree_destinatarios.insert("", "end", values=(row['nombre'], row['correo']))

    def actualizar_preview(self, event=None):
        archivo_nombre = self.plantilla1_var.get()
        if not archivo_nombre: return
        
        archivo_path = os.path.join("templates", archivo_nombre)
        if not os.path.exists(archivo_path): return
        
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logo_path = os.path.join('assets', 'Logo_blanco_ver3.png')
            logo_color_path = os.path.join('assets', 'Logo_y_texto_Partner_Tech.png')
            
            logo_base64_uri = get_base64_image(logo_path)
            logo_color_base64_uri = get_base64_image(logo_color_path)
            
            # --- CARGAR ICONOS PARA PREVIEW ---
            icon_agenda_uri = get_base64_image(os.path.join('assets', 'benefit_agenda.svg'))
            icon_historia_uri = get_base64_image(os.path.join('assets', 'benefit_historia.svg'))
            icon_liquidacion_uri = get_base64_image(os.path.join('assets', 'benefit_liquidacion.svg'))
            icon_reunion_uri = get_base64_image(os.path.join('assets', 'benefit_reunion.svg'))

            # Generar hash falso para la preview
            email_hash_preview = hashlib.md5(b"preview@admin.com").hexdigest()

            # Cargar HTML y aplicar reemplazos para la previsualización
            preview_content = content.replace('{{Nombre_Remitente}}', self.nombre_remitente_var.get())\
                                     .replace('{{Email_Remitente}}', self.email_remitente_var.get())\
                                     .replace('{{Cargo_Remitente}}', self.cargo_remitente_var.get())\
                                     .replace('{{Nombre_Contacto}}', "[Nombre Cliente]")\
                                     .replace('{{Email_Destinatario}}', "[Email Cliente]")\
                                     .replace('cid:Logo_ver1', logo_base64_uri)\
                                     .replace('cid:Logo_Color', logo_color_base64_uri)\
                                     .replace('cid:Icon_Agenda', icon_agenda_uri)\
                                     .replace('cid:Icon_Historia', icon_historia_uri)\
                                     .replace('cid:Icon_Liquidacion', icon_liquidacion_uri)\
                                     .replace('cid:Icon_Reunion', icon_reunion_uri)\
                                     .replace('{{MAX_WIDTH_PLACEHOLDER}}', 'max-width: none;')\
                                     .replace('{{Email_Hash}}', email_hash_preview)
            
            # self.visor_html.load_html(preview_content) # Ya no existe
        except Exception as e:
            self.log_msg(f"Error en preview: {e}", "ERROR")

    def verificar_formato(self, email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except: return False

    def enviar_correo(self, nombre, email_destinatario, archivo_html_nombre):
        try:
            # Rutas simples relativas al directorio del script
            archivo_html_path = os.path.abspath(os.path.join("templates", archivo_html_nombre))
            logo_path = os.path.join('assets', 'Logo_blanco_ver3.png')
            logo_color_path = os.path.join('assets', 'Logo_y_texto_Partner_Tech.png')
            with open(archivo_html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Datos del Remitente desde UI
            remitente_nombre = self.nombre_remitente_var.get()
            remitente_email = self.email_remitente_var.get()
            remitente_pass = self.pass_remitente_var.get()
            remitente_cargo = self.cargo_remitente_var.get()
            asunto_template = self.asunto_var.get()

            # Hash del email destino para GA4 Client ID
            email_hash = hashlib.md5(email_destinatario.encode('utf-8')).hexdigest()

            # Reemplazos en HTML
            html_content = html_content.replace('{{Nombre_Contacto}}', nombre)\
                                       .replace('{{Email_Destinatario}}', email_destinatario)\
                                       .replace('{{Nombre_Remitente}}', remitente_nombre)\
                                       .replace('{{Email_Remitente}}', remitente_email)\
                                       .replace('{{Cargo_Remitente}}', remitente_cargo)\
                                       .replace('{{Email_Hash}}', email_hash)
            
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
                # Adjuntar Logo Blanco (Logo_ver1)
                with open(logo_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<Logo_ver1>')
                    message.attach(img)
                
                # Adjuntar Logo Color (Logo_Color)
                with open(logo_color_path, 'rb') as f:
                    img_c = MIMEImage(f.read())
                    img_c.add_header('Content-ID', '<Logo_Color>')
                    message.attach(img_c)

                # --- ADJUNTAR ICONOS DE BENEFICIOS (SI EXISTEN) ---
                # Soporta tanto SVG como PNG (se busca primero .png por compatibilidad)
                iconos_beneficios = {
                    'benefit_agenda': 'Icon_Agenda',
                    'benefit_historia': 'Icon_Historia',
                    'benefit_liquidacion': 'Icon_Liquidacion',
                    'benefit_reunion': 'Icon_Reunion'
                }

                for base_name, cid_name in iconos_beneficios.items():
                    # Intentar encontrar PNG primero, luego SVG
                    icon_path = None
                    for ext in ['.png', '.svg']:
                        p = os.path.join('assets', base_name + ext)
                        if os.path.exists(p):
                            icon_path = p
                            break
                    
                    if icon_path:
                        with open(icon_path, 'rb') as f:
                            img_icon = MIMEImage(f.read())
                            img_icon.add_header('Content-ID', f'<{cid_name}>')
                            message.attach(img_icon)

            except Exception as e:
                self.log_msg(f"No se pudo adjuntar el logo o iconos: {e}", "WARNING")
            
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(remitente_email, remitente_pass)
                server.sendmail(remitente_email, email_destinatario, message.as_string())
            return True
        except Exception as e:
            self.log_msg(f"Error con {email_destinatario}: {e}", "ERROR")
            return False

    def iniciar_envio_thread(self):
        self.btn_iniciar.config(state="disabled")
        self.enviando = True
        threading.Thread(target=self.proceso_envio, daemon=True).start()

    def proceso_envio(self):
        # Recopilar plantillas seleccionadas
        plantillas_para_envio = []
        p1 = self.plantilla1_var.get()
        p2 = self.plantilla2_var.get()
        p3 = self.plantilla3_var.get()
        
        if p1: plantillas_para_envio.append(p1)
        if p2 and p2 != "Ninguna": plantillas_para_envio.append(p2)
        if p3 and p3 != "Ninguna": plantillas_para_envio.append(p3)

        log_csv = os.path.join('data', 'registro_envios.csv')
        
        if not self.archivo_excel_seleccionado:
            self.log_msg("Error: No se ha seleccionado ningún archivo de destinatarios.", "ERROR")
            messagebox.showerror("Error", "No se ha seleccionado ningún archivo de destinatarios.")
            self.enviando = False
            self.btn_iniciar.config(state="normal")
            self.status_var.set("Finalizado con error")
            return

        try:
            self.log_msg("--- INICIANDO ENVÍO MASIVO ---")
            df = pd.read_excel(self.archivo_excel_seleccionado).fillna('')
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
                
                # VERIFICACIÓN SQLITE
                if not self.es_elegible_envio(correo):
                    self.log_msg(f"Bloqueado (SQLite - Periodo reciente): {correo}", "WARNING")
                    continue

                # Selección de plantilla rotativa
                archivo_html_nombre = plantillas_para_envio[idx % len(plantillas_para_envio)]
                
                exito = self.enviar_correo(nombre, correo, archivo_html_nombre) # Pasamos solo el nombre
                estado = "Enviado" if exito else "Fallido"
                
                if exito:
                    self.registrar_envio_db(correo, archivo_html_nombre)

                with open(log_csv, 'a', encoding='utf-8') as f:
                    f.write(f'"{nombre}","{correo}","{archivo_html_nombre}","{time.strftime("%Y-%m-%d %H:%M:%S")}","{estado}"\n')
                
                # Loguear siempre el resultado
                resultado_msg = f"OK ({archivo_html_nombre}): {correo}" if exito else f"FALLÓ ({archivo_html_nombre}): {correo}"
                self.log_msg(resultado_msg)
                
                if idx + 1 < total:
                    # Lógica de pausas
                    if (idx + 1) % 50 == 0:
                        self.log_msg(f"Pausa de lote (5 min) al llegar a {idx+1} correos...")
                        time.sleep(300) # 5 minutos
                    else:
                        tiempo_espera = random.uniform(10, 15)
                        self.log_msg(f"Esperando {tiempo_espera:.2f}s...")
                        time.sleep(tiempo_espera)
            
            self.log_msg("--- PROCESO FINALIZADO ---")
            self.actualizar_stats_db()
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
