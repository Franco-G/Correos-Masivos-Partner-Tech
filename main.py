import pandas as pd
import smtplib
import ssl
import time
import random
import glob
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate, make_msgid
import logging
from email_validator import validate_email, EmailNotValidError
from tkinterweb import HtmlFrame
import sys
import pathlib

# --- FUNCIÓN PARA MANEJAR RUTAS EN PYINSTALLER ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CONFIGURACIÓN LOGGING ---
logging.basicConfig(
    filename='registro_envios.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- CONFIGURACIÓN ---
smtp_server = "mail.partnertech.pe"
smtp_port = 465
sender_email = "fguerrero@partnertech.pe"
password_email = "Franco001"

class CorreoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Partner Tech | Gestor de Envío Masivo")
        self.root.state('zoomed')
        self.root.geometry("1100x700")
        
        # Configurar Estilos
        self.setup_styles()
        self.root.configure(bg="#f4f6f9")

        # Variables de control
        self.plantilla_var = tk.StringVar()
        self.contador_var = tk.StringVar(value="Ningún archivo seleccionado")
        self.enviando = False
        self.archivo_excel_seleccionado = None
        
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
        
        # PESTAÑAS PRINCIPALES
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Panel de Envío (Lo que ya existía)
        self.tab_envio = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_envio, text=" 📨 Panel de Envío ")
        
        # Tab 2: Editor de Plantillas (Nuevo)
        self.tab_editor = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_editor, text=" ✍️ Editor de Plantillas ")
        
        # --- CONSTRUCCIÓN TAB 1: ENVÍO ---
        self.construir_tab_envio()
        
        # --- CONSTRUCCIÓN TAB 2: EDITOR ---
        self.construir_tab_editor()

        # Barra de estado
        self.status_var = tk.StringVar(value="Listo.")
        self.status_bar = tk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w", bg="#001556", fg="white", padx=10)
        self.status_bar.pack(side="bottom", fill="x")

        # Inicialización
        self.cargar_plantillas()
        self.contar_destinatarios()

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

        # --- SECCIÓN ENVÍO ---
        ttk.Label(frame_config, text="Plantilla:", style="Bold.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_plantillas = ttk.Combobox(frame_config, textvariable=self.plantilla_var, state="readonly")
        self.combo_plantillas.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.combo_plantillas.bind("<<ComboboxSelected>>", self.actualizar_preview)

        ttk.Label(frame_config, text="Asunto:", style="Bold.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        opciones_asunto = [
            "{{Nombre_Remitente}}: ¿Tu software actual te limita?",
            "Optimiza tus procesos - {{Nombre_Remitente}} (Partner Tech)",
            "{{Nombre_Remitente}}: Una pregunta breve sobre tu operación",
            "Propuesta de desarrollo a medida de {{Nombre_Remitente}}",
            "Hola {{Nombre_Contacto}}, soy {{Nombre_Remitente}} de Partner Tech"
        ]
        self.combo_asunto = ttk.Combobox(frame_config, textvariable=self.asunto_var, values=opciones_asunto)
        self.combo_asunto.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.combo_asunto.current(0)

        ttk.Label(frame_config, text="Archivo:", style="Bold.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.btn_cargar = ttk.Button(frame_config, text="📁 Seleccionar Excel...", command=self.cargar_archivo_excel)
        self.btn_cargar.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame_config, text="Destinatarios:", style="Bold.TLabel").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Label(frame_config, textvariable=self.contador_var).grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.btn_iniciar = ttk.Button(frame_config, text="🚀 INICIAR ENVÍO", command=self.iniciar_envio_thread, style="Action.TButton")
        self.btn_iniciar.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        self.btn_iniciar.config(state="disabled")

        # Logs
        frame_logs = ttk.LabelFrame(left_col, text="📝 Registro de Actividad", padding=10)
        frame_logs.pack(fill="both", expand=True)

        self.txt_log = scrolledtext.ScrolledText(frame_logs, state='disabled', height=10, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4")
        self.txt_log.pack(fill="both", expand=True)

        # PANEL CENTRAL: Visor Preview Real
        center_col = ttk.LabelFrame(main_paned_window, text="👁️ Vista Previa del Correo", padding=10)
        main_paned_window.add(center_col, weight=2)
        
        self.visor_html = HtmlFrame(center_col, messages_enabled=False)
        self.visor_html.pack(fill="both", expand=True)

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
        # Usamos resource_path para encontrar los HTMLs dentro del .exe
        ruta_busqueda = resource_path("*.html")
        archivos = glob.glob(ruta_busqueda)
        if archivos:
            # Mostramos solo el nombre del archivo, no la ruta completa
            self.combo_plantillas['values'] = [os.path.basename(f) for f in archivos]
            self.plantilla_var.set(os.path.basename(archivos[0])) # Usar la variable para setear
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
                df = pd.read_excel(self.archivo_excel_seleccionado)
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
        archivo_nombre = self.plantilla_var.get()
        if not archivo_nombre: return
        
        archivo_path = resource_path(archivo_nombre)
        if not os.path.exists(archivo_path): return
        
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logo_path = resource_path('Logo_blanco_ver1.png')
            logo_uri = pathlib.Path(logo_path).as_uri()
            
            # Cargar HTML en el visor real y reemplazar placeholders con datos de ejemplo del remitente
            preview_content = content.replace('{{Nombre_Remitente}}', self.nombre_remitente_var.get())\
                                     .replace('{{Email_Remitente}}', self.email_remitente_var.get())\
                                     .replace('{{Cargo_Remitente}}', self.cargo_remitente_var.get())\
                                     .replace('{{Nombre_Contacto}}', "[Nombre Cliente]")\
                                     .replace('{{Email_Destinatario}}', "[Email Cliente]")\
                                     .replace('cid:Logo_ver1', logo_uri)
            
            self.visor_html.load_html(preview_content)
        except Exception as e:
            self.log_msg(f"Error en preview: {e}", "ERROR")

    def verificar_formato(self, email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except: return False

    def construir_tab_editor(self):
        # Variables del Constructor
        self.bloques = [] # Lista de dicts {type, content, url, etc}
        self.timer_preview = None # Variable para debounce
        
        # LAYOUT: 3 COLUMNAS (Bloques, Propiedades, Preview)
        paned = ttk.PanedWindow(self.tab_editor, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 1. PANEL IZQUIERDO: Lista de Bloques y Botones de Agregar
        frame_left = ttk.Frame(paned, width=250)
        frame_left.pack_propagate(False)
        paned.add(frame_left, weight=0)
        
        # Botones de Agregar
        lbl_acciones = ttk.Label(frame_left, text="➕ Agregar Elemento", style="Bold.TLabel")
        lbl_acciones.pack(anchor="w", pady=(0,5))
        
        btn_add_titulo = ttk.Button(frame_left, text="H1  Título", command=lambda: self.agregar_bloque("TITULO"))
        btn_add_titulo.pack(fill="x", pady=2)
        
        btn_add_parrafo = ttk.Button(frame_left, text="¶   Párrafo", command=lambda: self.agregar_bloque("PARRAFO"))
        btn_add_parrafo.pack(fill="x", pady=2)
        
        btn_add_btn_verde = ttk.Button(frame_left, text="🟩 Botón Principal", command=lambda: self.agregar_bloque("BTN_VERDE"))
        btn_add_btn_verde.pack(fill="x", pady=2)
        
        btn_add_btn_azul = ttk.Button(frame_left, text="🟦 Botón Reunión", command=lambda: self.agregar_bloque("BTN_AZUL"))
        btn_add_btn_azul.pack(fill="x", pady=2)
        
        btn_add_beneficio = ttk.Button(frame_left, text="⭐ Beneficio", command=lambda: self.agregar_bloque("BENEFICIO"))
        btn_add_beneficio.pack(fill="x", pady=2)
        
        ttk.Separator(frame_left, orient="horizontal").pack(fill="x", pady=10)
        
        # Lista de Bloques Actuales
        lbl_estructura = ttk.Label(frame_left, text="📑 Estructura del Correo", style="Bold.TLabel")
        lbl_estructura.pack(anchor="w", pady=(0,5))
        
        self.listbox_bloques = tk.Listbox(frame_left, height=15, selectmode=tk.SINGLE, font=("Segoe UI", 9))
        self.listbox_bloques.pack(fill="both", expand=True)
        self.listbox_bloques.bind("<<ListboxSelect>>", self.seleccionar_bloque)
        
        frame_controles_lista = ttk.Frame(frame_left)
        frame_controles_lista.pack(fill="x", pady=5)
        ttk.Button(frame_controles_lista, text="⬆", width=3, command=lambda: self.mover_bloque(-1)).pack(side="left", padx=2)
        ttk.Button(frame_controles_lista, text="⬇", width=3, command=lambda: self.mover_bloque(1)).pack(side="left", padx=2)
        ttk.Button(frame_controles_lista, text="❌ Eliminar", command=self.eliminar_bloque).pack(side="right", padx=2)
        
        # Botones Globales
        ttk.Separator(frame_left, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(frame_left, text="💾 GUARDAR PLANTILLA", command=self.guardar_plantilla_visual, style="Action.TButton").pack(fill="x", pady=5)
        ttk.Button(frame_left, text="🗑️ Limpiar Todo", command=self.limpiar_editor).pack(fill="x")

        # 2. PANEL CENTRAL: Propiedades del Bloque
        frame_center = ttk.LabelFrame(paned, text="🛠️ Propiedades", width=300)
        frame_center.pack_propagate(False)
        paned.add(frame_center, weight=0)
        
        self.frame_propiedades = ttk.Frame(frame_center, padding=10)
        self.frame_propiedades.pack(fill="both", expand=True)
        # (El contenido de este frame cambiará dinámicamente)
        
        # 3. PANEL DERECHO: Preview
        frame_right = ttk.LabelFrame(paned, text="👁️ Vista Previa")
        paned.add(frame_right, weight=1)
        
        self.editor_preview = HtmlFrame(frame_right)
        self.editor_preview.pack(fill="both", expand=True)
        
        # Inicializar con un saludo por defecto
        # Inicializar con contenido por defecto (Brochure)
        self.cargar_contenido_por_defecto()

    def cargar_contenido_por_defecto(self):
        # Recrear la estructura de correo_brochure.html
        self.bloques = [
            {"tipo": "SALUDO", "contenido": "Hola {{Nombre_Contacto}},"},
            {"tipo": "PARRAFO", "contenido": "Te saluda {{Nombre_Remitente}}, de Partner Tech. He identificado tu contacto en el Directorio CCL.\nSabemos que a medida que una empresa crece, el software genérico (\"enlatado\") empieza a quedar chico: procesos lentos, datos desconectados y manuales operativos interminables."},
            {"tipo": "PARRAFO", "contenido": "En <strong>Partner Tech</strong>, no te pedimos que adaptes tu negocio al software. <span class=\"highlight\">Nosotros construimos el software exactamente como tu operación lo necesita.</span>"},
            {"tipo": "PARRAFO", "contenido": "Nuestra metodología se basa en un análisis profundo de tus flujos de trabajo actuales para identificar cuellos de botella y oportunidades de automatización, garantizando un retorno de inversión medible desde la primera fase de implementación."},
            {"tipo": "PARRAFO", "contenido": "¿Por qué elegir nuestra Fábrica de Software?"},
            {"tipo": "BENEFICIO", "titulo": "🛠️ Desarrollo 100% Personalizado", "contenido": "Diseñamos sistemas que automatizan <strong>tus reglas de negocio</strong> específicas, integrando áreas críticas (Finanzas, Logística, RRHH) sin fricción.", "color": "#00c853"},
            {"tipo": "BENEFICIO", "titulo": "🔐 Es tu Activo, no un Alquiler", "contenido": "A diferencia de las licencias eternas, nosotros <strong>te entregamos el código fuente</strong>. Tú eres dueño de tu tecnología y de tu futuro.", "color": "#0056b3"},
            {"tipo": "PARRAFO", "contenido": "Si estás evaluando desarrollar una solución propia o buscas aplicativos listos para implementar, te invito a revisar nuestro portafolio:"},
            {"tipo": "BTN_VERDE", "texto": "Descargar Brochure", "subtexto": "Desarrollo de Software Estratégico", "url": "https://drive.google.com/file/d/1bDlvyO8tNbv_yf_QzIZumZ-de6caU-Ey/view?usp=sharing"},
            {"tipo": "PARRAFO", "contenido": "¿Tienes un cuello de botella operativo que el software actual no resuelve?"},
            {"tipo": "BTN_AZUL", "texto": "📅 Agendar Reunión de 15 min", "url": "https://cal.com/negocios-partner-tech/requerimientos-software-desarrollo"},
            {"tipo": "PARRAFO", "contenido": "Diagnostiquemos si un desarrollo a medida es la inversión correcta para tu año 2026."}
        ]
        self.actualizar_lista_bloques()
        self.programar_actualizacion()

    def agregar_bloque(self, tipo, inicial=False):
        bloque = {"tipo": tipo}
        
        if tipo == "TITULO":
            bloque["contenido"] = "Escribe tu título aquí"
        elif tipo == "PARRAFO":
            bloque["contenido"] = "Escribe tu párrafo aquí..."
        elif tipo == "BTN_VERDE":
            bloque["texto"] = "Descargar Brochure"
            bloque["url"] = "https://"
        elif tipo == "BTN_AZUL":
            bloque["texto"] = "📅 Agendar Reunión"
            bloque["url"] = "https://cal.com/..."
        elif tipo == "SALUDO":
            bloque["contenido"] = "Hola {{Nombre_Contacto}},"
        elif tipo == "BENEFICIO":
            bloque["titulo"] = "Título del Beneficio"
            bloque["contenido"] = "Descripción del beneficio..."
            bloque["color"] = "#00c853"
            
        self.bloques.append(bloque)
        self.actualizar_lista_bloques()
        if not inicial:
            self.listbox_bloques.selection_clear(0, tk.END)
            self.listbox_bloques.selection_set(tk.END)
            self.seleccionar_bloque()
        self.programar_actualizacion()

    def actualizar_lista_bloques(self):
        self.listbox_bloques.delete(0, tk.END)
        for i, b in enumerate(self.bloques):
            if b["tipo"] == "TITULO": icon = "H1 "
            elif b["tipo"] == "PARRAFO": icon = "¶  "
            elif b["tipo"] == "BTN_VERDE": icon = "🟩 "
            elif b["tipo"] == "BTN_AZUL": icon = "🟦 "
            elif b["tipo"] == "SALUDO": icon = "👋 "
            elif b["tipo"] == "BENEFICIO": icon = "⭐ "
            else: icon = "?  "
            
            texto = b.get("contenido", b.get("texto", b.get("titulo", "")))
            if len(texto) > 25: texto = texto[:25] + "..."
            self.listbox_bloques.insert(tk.END, f"{i+1}. {icon} {texto}")

    def seleccionar_bloque(self, event=None):
        seleccion = self.listbox_bloques.curselection()
        if not seleccion: return
        
        idx = seleccion[0]
        bloque = self.bloques[idx]
        
        # Limpiar panel propiedades
        for widget in self.frame_propiedades.winfo_children():
            widget.destroy()
            
        ttk.Label(self.frame_propiedades, text=f"Editando Bloque {idx+1}", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0,10))
        
        if bloque["tipo"] in ["TITULO", "PARRAFO", "SALUDO"]:
            self.crear_toolbar_texto(self.frame_propiedades)
            
            ttk.Label(self.frame_propiedades, text="Contenido:").pack(anchor="w")
            txt = tk.Text(self.frame_propiedades, height=10, width=30, font=("Segoe UI", 10))
            self.configurar_tags_texto(txt)
            self.insertar_html_en_texto(txt, bloque["contenido"])
            txt.pack(fill="both", expand=True, pady=5)
            # Guardar cambios al soltar tecla
            txt.bind("<KeyRelease>", lambda e: self.actualizar_bloque_texto_rich(idx, txt))
            
            self.toolbar_btn_bold.configure(command=lambda: self.toggle_negrilla(txt))

            # Botón helper para variable
            ttk.Button(self.frame_propiedades, text="Insertar {{Nombre_Contacto}}", 
                        command=lambda: [txt.insert(tk.INSERT, "{{Nombre_Contacto}}"), self.actualizar_bloque_texto_rich(idx, txt, force=True)]
                        ).pack(fill="x")

        elif bloque["tipo"] in ["BTN_VERDE", "BTN_AZUL"]:
            ttk.Label(self.frame_propiedades, text="Texto del Botón:").pack(anchor="w")
            var_texto = tk.StringVar(value=bloque["texto"])
            entry_texto = ttk.Entry(self.frame_propiedades, textvariable=var_texto)
            entry_texto.pack(fill="x", pady=5)
            entry_texto.bind("<KeyRelease>", lambda e: self.actualizar_bloque_btn_delayed(idx, "texto", var_texto.get()))

            ttk.Label(self.frame_propiedades, text="URL del Botón:").pack(anchor="w")
            var_url = tk.StringVar(value=bloque["url"])
            entry_url = ttk.Entry(self.frame_propiedades, textvariable=var_url)
            entry_url.pack(fill="x", pady=5)
            entry_url.bind("<KeyRelease>", lambda e: self.actualizar_bloque_btn_delayed(idx, "url", var_url.get()))

            ttk.Label(self.frame_propiedades, text="Subtexto (Opcional):").pack(anchor="w", pady=(10,0))
            var_sub = tk.StringVar(value=bloque.get("subtexto", ""))
            entry_sub = ttk.Entry(self.frame_propiedades, textvariable=var_sub)
            entry_sub.pack(fill="x", pady=5)
            entry_sub.bind("<KeyRelease>", lambda e: self.actualizar_bloque_btn_delayed(idx, "subtexto", var_sub.get()))

        elif bloque["tipo"] == "BENEFICIO":
            ttk.Label(self.frame_propiedades, text="Título:").pack(anchor="w")
            var_titulo = tk.StringVar(value=bloque["titulo"])
            entry_titulo = ttk.Entry(self.frame_propiedades, textvariable=var_titulo)
            entry_titulo.pack(fill="x", pady=5)
            entry_titulo.bind("<KeyRelease>", lambda e: self.actualizar_bloque_btn_delayed(idx, "titulo", var_titulo.get()))

            ttk.Label(self.frame_propiedades, text="Contenido:").pack(anchor="w", pady=(10,0))
            self.crear_toolbar_texto(self.frame_propiedades)
            
            txt = tk.Text(self.frame_propiedades, height=5, width=30, font=("Segoe UI", 10))
            self.configurar_tags_texto(txt)
            self.insertar_html_en_texto(txt, bloque["contenido"])
            txt.pack(fill="both", expand=True, pady=5)
            txt.bind("<KeyRelease>", lambda e: self.actualizar_bloque_texto_rich(idx, txt))
            self.toolbar_btn_bold.configure(command=lambda: self.toggle_negrilla(txt))

            ttk.Label(self.frame_propiedades, text="Color Borde (Hex):").pack(anchor="w", pady=(10,0))
            var_color = tk.StringVar(value=bloque.get("color", "#00c853"))
            entry_color = ttk.Entry(self.frame_propiedades, textvariable=var_color)
            entry_color.pack(fill="x", pady=5)
            entry_color.bind("<KeyRelease>", lambda e: self.actualizar_bloque_btn_delayed(idx, "color", var_color.get()))

    # --- MÉTODOS RICH TEXT ---
    def crear_toolbar_texto(self, parent):
        frame_tools = ttk.Frame(parent)
        frame_tools.pack(fill="x", pady=(0, 2))
        self.toolbar_btn_bold = ttk.Button(frame_tools, text="𝗕", width=3, style="Tool.TButton")
        self.toolbar_btn_bold.pack(side="left")

    def configurar_tags_texto(self, text_widget):
        text_widget.tag_configure("bold", font=("Segoe UI", 10, "bold"))

    def toggle_negrilla(self, text_widget):
        try:
            current_tags = text_widget.tag_names("sel.first")
            if "bold" in current_tags:
                text_widget.tag_remove("bold", "sel.first", "sel.last")
            else:
                text_widget.tag_add("bold", "sel.first", "sel.last")
            # Disparar actualización
            self.actualizar_bloque_texto_rich(None, text_widget) # idx se maneja en el bind original, esto es click manual
        except tk.TclError:
            pass # No selection

    def insertar_html_en_texto(self, text_widget, html_content):
        # Convertir <strong>...</strong> a tags de tkinter
        parts = html_content.split("<strong>")
        for i, part in enumerate(parts):
            if "</strong>" in part:
                bold_text, normal_text = part.split("</strong>", 1)
                text_widget.insert(tk.END, bold_text, "bold")
                text_widget.insert(tk.END, normal_text)
            else:
                text_widget.insert(tk.END, part)

    def extraer_html_de_texto(self, text_widget):
        content = text_widget.get("1.0", "end-1c")
        # Esta es una implementación simplificada. 
        # Para hacerlo robusto iteramos rangos:
        html_out = ""
        index = "1.0"
        while True:
            next_bold = text_widget.tag_nextrange("bold", index)
            if not next_bold:
                html_out += text_widget.get(index, "end-1c")
                break
            
            start, end = next_bold
            if text_widget.compare(start, ">", index):
                html_out += text_widget.get(index, start)
            
            html_out += "<strong>" + text_widget.get(start, end) + "</strong>"
            index = end
            
        return html_out

    def actualizar_bloque_texto_rich(self, idx, text_widget, force=False):
        # Si viene de toggle_negrilla, idx puede ser None, necesitamos recuperar el idx activo
        if idx is None:
            sel = self.listbox_bloques.curselection()
            if not sel: return
            idx = sel[0]
            
        contenido = self.extraer_html_de_texto(text_widget)
        self.bloques[idx]["contenido"] = contenido
        if force:
            self.actualizar_preview_visual()
        else:
            self.programar_actualizacion()

    def actualizar_bloque_texto_delayed(self, idx, contenido, force=False):
        self.bloques[idx]["contenido"] = contenido
        if force:
            self.actualizar_preview_visual()
        else:
            self.programar_actualizacion()
        
    def actualizar_bloque_btn_delayed(self, idx, clave, valor):
        self.bloques[idx][clave] = valor
        self.actualizar_lista_bloques() # Título cambia inmediato
        self.programar_actualizacion()

    def programar_actualizacion(self):
        if self.timer_preview:
            self.root.after_cancel(self.timer_preview)
        self.timer_preview = self.root.after(800, self.actualizar_preview_visual)

    def mover_bloque(self, direccion):
        sel = self.listbox_bloques.curselection()
        if not sel: return
        idx = sel[0]
        if 0 <= idx + direccion < len(self.bloques):
            self.bloques[idx], self.bloques[idx+direccion] = self.bloques[idx+direccion], self.bloques[idx]
            self.actualizar_lista_bloques()
            self.listbox_bloques.selection_set(idx+direccion)
            self.actualizar_preview_visual()

    def eliminar_bloque(self):
        sel = self.listbox_bloques.curselection()
        if not sel: return
        idx = sel[0]
        if self.bloques[idx]["tipo"] == "SALUDO":
            messagebox.showwarning("Aviso", "No se recomienda borrar el saludo inicial.")
            return
        del self.bloques[idx]
        self.actualizar_lista_bloques()
        self.actualizar_preview_visual()
        
        # Limpiar propiedades
        for widget in self.frame_propiedades.winfo_children(): widget.destroy()

    def limpiar_editor(self):
        if messagebox.askyesno("Confirmar", "¿Borrar todo el contenido actual?"):
            self.bloques = []
            self.cargar_contenido_por_defecto()

    def generar_html_final(self):
        # Base HTML (Header y Estilos)
        html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Correo Partner Tech</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; font-family: 'Poppins', sans-serif; background-color: #f4f7f6; color: #555; }
        .wrapper { width: 100%; table-layout: fixed; background-color: #f4f7f6; padding: 40px 0; }
        .main-container { background-color: #ffffff; margin: 0 auto; width: 100%; max-width: 600px; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06); }
        .content { padding: 40px 35px; }
        .greeting { font-size: 20px; color: #2c3e50; font-weight: 700; margin-bottom: 20px; font-family: 'Orbitron', sans-serif; }
        .text-paragraph { font-size: 16px; line-height: 1.7; color: #666; margin-bottom: 25px; }
        
        .btn-primary { 
            background-color: #00c853; 
            color: #ffffff !important; 
            display: block; 
            width: 100%; 
            max-width: 380px; 
            margin: 0 auto 15px auto; 
            padding: 14px 30px; 
            text-decoration: none; 
            border-radius: 50px; 
            font-weight: 700; 
            font-size: 16px; 
            text-align: center; 
            font-family: 'Poppins', sans-serif; 
            box-shadow: 0 4px 12px rgba(0, 200, 83, 0.3); 
            transition: all 0.3s ease; 
        }
        .btn-meeting { 
            background-color: #0056b3; 
            color: #ffffff !important; 
            display: block; 
            width: 100%; 
            max-width: 380px; 
            margin: 0 auto 15px auto; 
            padding: 14px 30px; 
            text-decoration: none; 
            border-radius: 50px; 
            font-weight: 700; 
            font-size: 15px; 
            text-align: center; 
            font-family: 'Poppins', sans-serif; 
            box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3); 
            transition: all 0.3s ease; 
        }
        
        .btn-primary:hover { background-color: #00b34a; transform: translateY(-2px); }
        .btn-meeting:hover { background-color: #004494; transform: translateY(-2px); }

        .closing-box { text-align: center; margin-top: 35px; padding-top: 25px; border-top: 1px dashed #dce5f2; }
        .footer { background-color: #2d3748; padding: 30px; text-align: center; font-size: 13px; color: #555; }
        .footer-logo { max-height: 80px; width: auto; margin: 10px auto 0; display: block; }
        .footer a { color: #cbd5e0; text-decoration: none; border-bottom: 1px dotted #cbd5e0; }

        /* NUEVOS ESTILOS BROCHURE */
        .highlight { color: #0056b3; font-weight: 700; }
        
        .benefit-box {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 5px solid #00c853;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        }
        .benefit-title {
            color: #2c3e50;
            font-size: 16px;
            font-weight: 700;
            display: block;
            margin-bottom: 5px;
            font-family: 'Orbitron', sans-serif;
        }
        .benefit-text {
            font-size: 14px;
            line-height: 1.5;
            color: #718096;
            margin: 0;
            font-family: 'Poppins', sans-serif;
        }
        .btn-section {
            background-color: #f8fafc;
            border-radius: 12px;
            padding: 30px 20px;
            margin: 30px 0;
            text-align: center;
            border: 1px solid #edf2f7;
        }
        .btn-label {
            display: block; font-size: 14px; color: #555; margin-bottom: 15px;
            font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
        }
        .btn-subtext {
            font-size: 12px; font-weight: 400; opacity: 0.95; display: block;
            margin-top: 3px; font-family: 'Poppins', sans-serif;
        }
        .call-action {
            font-size: 17px; color: #0056b3; font-weight: 700;
            margin-bottom: 10px; font-family: 'Orbitron', sans-serif;
        }
    </style>
</head>
<body>
    <center class="wrapper">
        <table class="main-container" cellpadding="0" cellspacing="0">
            <tr>
                <td class="content">
"""
        # Inyectar Bloques
        for b in self.bloques:
            if b["tipo"] == "SALUDO":
                html += f'                    <p class="greeting">{b["contenido"]}</p>\n'
            elif b["tipo"] == "TITULO":
                html += f'                    <h2 style="color:#2c3e50; font-family:Orbitron, sans-serif; margin-bottom:20px;">{b["contenido"]}</h2>\n'
            elif b["tipo"] == "PARRAFO":
                # Convertir saltos de línea a <br>
                texto = b["contenido"].replace("\n", "<br>")
                html += f'                    <p class="text-paragraph">{texto}</p>\n'
            elif b["tipo"] == "BTN_VERDE":
                sub = f'<span class="btn-subtext" style="font-size: 12px; font-weight: 400; opacity: 0.95; display: block; margin-top: 3px; font-family: \'Poppins\', sans-serif;">{b.get("subtexto", "")}</span>' if b.get("subtexto") else ""
                html += f'                    <a href="{b["url"]}" class="btn-primary" style="background-color: #00c853; color: #ffffff !important; display: block; width: 100%; max-width: 380px; margin: 0 auto 15px auto; padding: 14px 30px; text-decoration: none; border-radius: 50px; font-weight: 700; font-size: 16px; text-align: center; font-family: \'Poppins\', sans-serif; box-shadow: 0 4px 12px rgba(0, 200, 83, 0.3);"><span style="color: #ffffff;">{b["texto"]}</span>{sub}</a>\n'
            elif b["tipo"] == "BTN_AZUL":
                sub = f'<span class="btn-subtext" style="font-size: 12px; font-weight: 400; opacity: 0.95; display: block; margin-top: 3px; font-family: \'Poppins\', sans-serif;">{b.get("subtexto", "")}</span>' if b.get("subtexto") else ""
                html += f'                    <a href="{b["url"]}" class="btn-meeting" style="background-color: #0056b3; color: #ffffff !important; display: block; width: 100%; max-width: 380px; margin: 0 auto 15px auto; padding: 14px 30px; text-decoration: none; border-radius: 50px; font-weight: 700; font-size: 15px; text-align: center; font-family: \'Poppins\', sans-serif; box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);"><span style="color: #ffffff;">{b["texto"]}</span>{sub}</a>\n'
            elif b["tipo"] == "BENEFICIO":
                color = b.get("color", "#00c853")
                html += f'''                    <div class="benefit-box" style="border-left-color: {color};">
                        <span class="benefit-title">{b["titulo"]}</span>
                        <p class="benefit-text">{b["contenido"]}</p>
                    </div>\n'''

        # Cierre Fijo (Firma + Footer)
        html += """
                    <div class="closing-box">
                        <p style="color: #555; margin-top: 15px; margin-bottom: 10px;">
                            Saludos,<br><strong>{{Nombre_Remitente}}</strong><br>
                            <a href="mailto:{{Email_Remitente}}" style="color: #0056b3; text-decoration: none;">{{Email_Remitente}}</a><br>
                            <span style="font-size: 14px; color: #888;">{{Cargo_Remitente}} | Partner Tech</span>
                        </p>
                        <img src="cid:Logo_ver1" alt="Partner Tech Logo" class="footer-logo">
                    </div>
                </td>
            </tr>
            <tr>
                <td class="footer">
                    <p>Enviado a <strong>{{Email_Destinatario}}</strong> cumpliendo los lineamientos de la <strong>Cámara de Comercio de Lima (CCL)</strong>.</p>
                    <p>Respetamos tu privacidad profesional. Si no deseas recibir más correos, <a href="mailto:negocios@partnertech.pe?subject=Remover">haga clic aquí para darse de baja</a>.</p>
                    <p style="margin-top: 15px;">RUC 20523799623 | Partnertech.pe | Av. Malachowsky 340, San Borja, Lima</p>
                </td>
            </tr>
        </table>
    </center>
</body>
</html>"""
        return html

    def actualizar_preview_visual(self):
        html = self.generar_html_final()
        logo_path = resource_path('Logo_blanco_ver1.png')
        logo_uri = pathlib.Path(logo_path).as_uri()
        # Preview dummy
        preview = html.replace('{{Nombre_Remitente}}', self.nombre_remitente_var.get())\
                      .replace('{{Cargo_Remitente}}', self.cargo_remitente_var.get())\
                      .replace('{{Email_Remitente}}', self.email_remitente_var.get())\
                      .replace('{{Nombre_Contacto}}', "[Cliente]")\
                      .replace('{{Email_Destinatario}}', "[Email]")\
                      .replace('cid:Logo_ver1', logo_uri)
        self.editor_preview.load_html(preview)

    def guardar_plantilla_visual(self):
        filename = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if filename:
            html = self.generar_html_final()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            messagebox.showinfo("Guardado", "Plantilla guardada correctamente.")
            self.cargar_plantillas()

    def enviar_correo(self, nombre, email_destinatario, archivo_html_nombre):
        try:
            # Obtener la ruta completa de la plantilla y el logo
            archivo_html_path = resource_path(archivo_html_nombre)
            logo_path = resource_path('Logo_blanco_ver1.png')

            with open(archivo_html_path, 'r', encoding='utf-8') as f:
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
                with open(logo_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<Logo_ver1>')
                    message.attach(img)
            except Exception as e:
                self.log_msg(f"No se pudo adjuntar el logo: {e}", "WARNING")
            
            context = ssl.create_default_context()
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
        archivo_html_nombre = self.plantilla_var.get() # <-- Solo el nombre del archivo
        log_csv = 'registro_envios.csv'
        
        if not self.archivo_excel_seleccionado:
            self.log_msg("Error: No se ha seleccionado ningún archivo de destinatarios.", "ERROR")
            messagebox.showerror("Error", "No se ha seleccionado ningún archivo de destinatarios.")
            self.enviando = False
            self.btn_iniciar.config(state="normal")
            self.status_var.set("Finalizado con error")
            return

        try:
            self.log_msg("--- INICIANDO ENVÍO MASIVO ---")
            df = pd.read_excel(self.archivo_excel_seleccionado)
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
                
                exito = self.enviar_correo(nombre, correo, archivo_html_nombre) # Pasamos solo el nombre
                estado = "Enviado" if exito else "Fallido"
                
                with open(log_csv, 'a', encoding='utf-8') as f:
                    f.write(f'"{nombre}","{correo}","{archivo_html_nombre}","{time.strftime("%Y-%m-%d %H:%M:%S")}","{estado}"\n')
                
                # Loguear siempre el resultado
                resultado_msg = f"OK: {correo}" if exito else f"FALLÓ: {correo}"
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
