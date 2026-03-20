# Informe de Validacion - Gestor de Envio Masivo de Correos

**Fecha:** 20 de marzo de 2026
**Archivo Analizado:** `src/main.py`
**Lineas de Codigo:** 946
**Lenguaje:** Python 3.x con Tkinter

---

## 1. Resumen Ejecutivo

El aplicativo es un gestor de envio masivo de correos electronicos con interfaz grafica (Tkinter) disenado para la empresa Partner Tech. Permite seleccionar plantillas HTML, cargar destinatarios desde archivos Excel, realizar seguimiento de envios mediante SQLite, y gestionar multiples perfiles de remitentes.

### Estado General de Salud: CRITICO

El codigo presenta **problemas graves de seguridad** que deben abordarse de manera inmediata antes de cualquier despliegue en produccion. Los hallazgos mas criticos incluyen:

- Credenciales hardcodeadas expuestas en el codigo fuente
- Verificacion SSL deshabilitada
- Contrasenas de usuarios almacenadas en texto plano

Ademas, existen problemas de diseno que afectan la mantenibilidad y escalabilidad del sistema, aunque la funcionalidad principal opera correctamente.

### Metricas de Evaluacion

| Categoria | Puntuacion | Estado |
|-----------|------------|--------|
| Seguridad | 2/10 | Critico |
| Performance | 6/10 | Aceptable |
| Calidad de Codigo | 5/10 | Mejorable |
| Manejo de Errores | 5/10 | Mejorable |
| Documentacion | 3/10 | Deficiente |

---

## 2. Problemas Encontrados

### CRITICOS

#### 2.1 Credenciales Hardcodeadas (Lineas 47-50)
**Severidad:** CRITICO
**Ubicacion:** Lineas 47-50

```python
smtp_server = "mail.partnertech.pe"
smtp_port = 465
sender_email = "fguerrero@partnertech.pe"
password_email = "Franco001"
```

**Problema:** Las credenciales del servidor SMTP estan expuestas directamente en el codigo fuente. Esto representa un riesgo de seguridad severo:
- El codigo fuente puede ser compartido o versionado inadvertidamente
- Las credenciales quedan expuestas en el repositorio de git
- No es posible rotar credenciales sin modificar el codigo

**Impacto:** Exposicion de credenciales de email corporativo, posible envio de spam desde la cuenta comprometida.

---

#### 2.2 Perfiles de Usuario con Contrasenas en Texto Plano (Lineas 124-135)
**Severidad:** CRITICO
**Ubicacion:** Lineas 124-135

```python
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
```

**Problema:** Las contrasenas de los usuarios se almacenan en texto plano dentro del codigo. Ademas, la variable `password_email` (linea 50) nunca se utiliza, quedando expuesta sin proposito.

**Impacto:** Exposicion de credenciales de empleados, violacion de politicas de seguridad, riesgo de acceso no autorizado.

---

#### 2.3 Verificacion SSL Deshabilitada (Lineas 848-850)
**Severidad:** CRITICO
**Ubicacion:** Lineas 848-850

```python
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
```

**Problema:** Se desactiva explicitamente la verificacion del certificado SSL y del hostname. Esto permite ataques de Man-in-the-Middle (MITM).

**Impacto:** Interceptacion de comunicaciones, robo de credenciales, modificacion de correos en transito.

---

### ALTOS

#### 2.4 Hash MD5 para Tracking (Linea 726)
**Severidad:** ALTO
**Ubicacion:** Linea 726

```python
email_hash = hashlib.md5(email_destinatario.encode('utf-8')).hexdigest()
```

**Problema:** MD5 es un algoritmo criptograficamente roto. Aunque se usa para identificadores de tracking y no para seguridad, MD5 permite colisiones y no deberia usarse.

**Recomendacion:** Usar SHA-256 o UUID para identificadores unicos.

---

#### 2.5 Threading con Tkinter (Lineas 355, 862)
**Severidad:** ALTO
**Ubicacion:** Lineas 355, 862

```python
threading.Thread(target=self.proceso_envio_prueba, args=(destinatario, plantillas_seleccionadas), daemon=True).start()
threading.Thread(target=self.proceso_envio, daemon=True).start()
```

**Problema:** Tkinter no es thread-safe. Los hilos modifican elementos de UI (`self.btn_enviar_prueba.config()`, `self.log_msg()`) desde threads secundarios, lo que puede causar:
- Race conditions
- Bloqueos de la interfaz
- Comportamiento impredecible
- Crashes aleatorios

**Impacto:** Inestabilidad de la aplicacion, perdida de datos de envio, mala experiencia de usuario.

---

#### 2.6 Manejo de Excepciones Insuficiente (Linea 707, 509)
**Severidad:** ALTO
**Ubicacion:** Linea 707

```python
except: return False
```

**Problema:** Clausulas `except` sin tipo especificado atrapan todas las excepciones, incluyendo `KeyboardInterrupt` y `SystemExit`, ocultando errores reales.

---

#### 2.7 Sin Validacion de Rutas de Archivo
**Severidad:** ALTO
**Ubicacion:** Funcion `cargar_archivo_excel()` (Lineas 592-601)

**Problema:** No hay validacion del tipo de archivo ni de la ruta. Un usuario podria intentar cargar archivos maliciosos con nombres que contengan caracteres especiales.

---

### MEDIOS

#### 2.8 Conexiones a Base de Datos No Optimizadas
**Severidad:** MEDIO
**Ubicacion:** Multiples funciones (`es_elegible_envio`, `registrar_envio_db`, `guardar_config_dias`)

**Problema:** Se abre una nueva conexion SQLite para cada operacion en lugar de mantener una conexion persistente o usar un pool de conexiones. Esto es ineficiente y puede causar problemas de rendimiento con muchos envios.

**Impacto:** Degradacion de rendimiento con volumenes altos de envios.

---

#### 2.9 CSV Log Sin Escape Adecuado (Linea 915-916)
**Severidad:** MEDIO
**Ubicacion:** Lineas 915-916

```python
with open(log_csv, 'a', encoding='utf-8') as f:
    f.write(f'"{nombre}","{correo}","{archivo_html_nombre}","{time.strftime("%Y-%m-%d %H:%M:%S")}","{estado}"\n')
```

**Problema:** Los campos CSV no se escapan correctamente. Si un nombre contiene comillas o comas, el CSV quedara corrupto.

---

#### 2.10 Valores Magicos Hardcodeados
**Severidad:** MEDIO
**Ubicacion:** Multiples puntos

```python
time.sleep(300)  # 5 minutos - Linea 926
random.uniform(10, 15)  # Espera aleatoria - Lineas 369, 928
```

**Problema:** Los valores de configuracion (tiempos de espera, pausas) estan hardcodeados. Deberian ser configurables.

---

#### 2.11 Sin Pooling de Plantillas HTML
**Severidad:** MEDIO
**Ubicacion:** Funcion `enviar_correo()` (Lineas 709-857)

**Problema:** Se lee el archivo HTML del disco para cada correo enviado. En envios masivos, esto causa I/O innecesario.

**Impacto:** Reduccion de rendimiento en envios grandes.

---

### BAJOS

#### 2.12 Falta de Documentacion (Docstrings)
**Severidad:** BAJO
**Ubicacion:** Todo el archivo

**Problema:** Las funciones carecen de docstrings que describan su proposito, parametros y valores de retorno.

---

#### 2.13 Variable No Utilizada
**Severidad:** BAJO
**Ubicacion:** Linea 50

```python
password_email = "Franco001"  # Nunca se usa
```

---

#### 2.14 Nombres de Variables Inconsistentes
**Severidad:** BAJO
**Ubicacion:** Todo el archivo

**Problema:** Mezcla de ingles y espanol en nombres de variables (`plantillas_test_vars` vs `lookup_correos`).

---

#### 2.15 Archivo Monolitico
**Severidad:** BAJO
**Ubicacion:** Todo el archivo

**Problema:** Todo el codigo (946 lineas) esta en un solo archivo. Deberia modularizarse en:
- `models/` - Clases de datos
- `services/` - Logica de envio, base de datos
- `ui/` - Componentes de interfaz
- `utils/` - Utilidades
- `config/` - Configuracion

---

## 3. Recomendaciones de Mejora

### Prioridad Inmediata (1-7 dias)

1. **Mover credenciales a variables de entorno**
   - Usar archivo `.env` (ya existe en el proyecto)
   - Cargar con `python-dotenv`
   - Nunca commitear el archivo `.env`

2. **Eliminar contrasenas del codigo fuente**
   - Implementar sistema de autenticacion seguro
   - Usar gestor de secretos o archivo de configuracion encriptado

3. **Habilitar verificacion SSL**
   - Eliminar las lineas que desactivan la verificacion
   - Usar certificados validos del servidor

4. **Corregir threading con Tkinter**
   - Usar `root.after()` para actualizaciones de UI
   - Implementar cola de mensajes thread-safe

### Prioridad Alta (1-4 semanas)

5. **Implementar conexion persistente a SQLite**
   - Crear clase `DatabaseManager` con conexion reutilizable
   - Implementar contexto `with` para manejo automatico

6. **Mejorar manejo de excepciones**
   - Especificar tipos de excepcion esperados
   - Loguear errores completos con traceback

7. **Validar entradas de usuario**
   - Validar rutas de archivo
   - Sanitizar nombres y correos

### Prioridad Media (1-2 meses)

8. **Refactorizar a arquitectura modular**
   - Separar responsabilidades en modulos
   - Implementar patron MVC/MVP

9. **Implementar sistema de configuracion**
   - Archivo `config.yaml` o `settings.json`
   - Valores por defecto con override

10. **Mejorar logging**
    - Rotacion de logs
    - Niveles de log configurables
    - Log estructurado (JSON)

---

## 4. Codigo Sugerido

### 4.1 Configuracion Segura con Variables de Entorno

```python
# config.py
import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class SMTPConfig:
    server: str = os.getenv('SMTP_SERVER', 'mail.partnertech.pe')
    port: int = int(os.getenv('SMTP_PORT', '465'))

    @classmethod
    def get_credentials(cls, profile_name: str) -> tuple[str, str]:
        """Obtiene credenciales desde variables de entorno segun el perfil."""
        profiles = {
            'Franco Guerrero': ('SMTP_USER_FRANCO', 'SMTP_PASS_FRANCO'),
            'Alexandra Cardozo': ('SMTP_USER_ALEX', 'SMTP_PASS_ALEX'),
        }
        if profile_name not in profiles:
            raise ValueError(f"Perfil desconocido: {profile_name}")

        user_key, pass_key = profiles[profile_name]
        email = os.getenv(user_key)
        password = os.getenv(pass_key)

        if not email or not password:
            raise ValueError(f"Credenciales no configuradas para {profile_name}")

        return email, password
```

Archivo `.env` (NO incluir en git):
```
SMTP_SERVER=mail.partnertech.pe
SMTP_PORT=465
SMTP_USER_FRANCO=fguerrero@partnertech.pe
SMTP_PASS_FRANCO=Franco001
SMTP_USER_ALEX=acardozo@partnertech.pe
SMTP_PASS_ALEX=acardozo001
```

---

### 4.2 Correccion de Threading Seguro

```python
import queue
import threading

class CorreoApp:
    def __init__(self, root: tk.Tk):
        # ... codigo existente ...
        self.message_queue = queue.Queue()
        self.root.after(100, self._process_queue)

    def _process_queue(self):
        """Procesa mensajes de la cola de forma thread-safe."""
        try:
            while True:
                msg = self.message_queue.get_nowait()
                self._update_ui(msg)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._process_queue)

    def _update_ui(self, msg: dict):
        """Actualiza la UI con un mensaje. Solo llamar desde el main thread."""
        if msg['type'] == 'log':
            self.log_msg(msg['message'], msg.get('level', 'INFO'))
        elif msg['type'] == 'status':
            self.status_var.set(msg['message'])
        elif msg['type'] == 'button':
            msg['button'].config(state=msg['state'])

    def log_msg_threadsafe(self, mensaje: str, nivel: str = "INFO"):
        """Log thread-safe que puede llamarse desde cualquier hilo."""
        self.message_queue.put({
            'type': 'log',
            'message': mensaje,
            'level': nivel
        })

    def proceso_envio_threadsafe(self):
        """Version thread-safe del proceso de envio."""
        # En lugar de modificar UI directamente:
        # self.btn_iniciar.config(state="disabled")  # INCORRECTO
        self.message_queue.put({'type': 'button', 'button': self.btn_iniciar, 'state': 'disabled'})

        try:
            # ... logica de envio ...
            self.log_msg_threadsafe("--- INICIANDO ENVIO MASIVO ---")
        finally:
            self.message_queue.put({'type': 'button', 'button': self.btn_iniciar, 'state': 'normal'})
```

---

### 4.3 Conexion a Base de Datos Optimizada

```python
import sqlite3
from contextlib import contextmanager
from threading import Lock
from dataclasses import dataclass
from datetime import datetime

class DatabaseManager:
    """Gestor de conexion a SQLite thread-safe y optimizado."""

    _instance = None
    _lock = Lock()

    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path: str = None):
        if self._initialized:
            return

        if db_path is None:
            os.makedirs('data', exist_ok=True)
            db_path = os.path.join('data', 'control_envios.db')

        self.db_path = db_path
        self._local = threading.local()
        self._initialized = True
        self._init_schema()

    @property
    def conn(self) -> sqlite3.Connection:
        """Retorna una conexion thread-local."""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path)
        return self._local.conn

    @contextmanager
    def get_cursor(self):
        """Context manager para obtener cursor de forma segura."""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def _init_schema(self):
        """Inicializa el schema de la base de datos."""
        with self.get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS envios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    correo TEXT NOT NULL,
                    fecha_ultimo_envio TIMESTAMP NOT NULL,
                    plantilla TEXT
                )
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_envios_correo
                ON envios(correo, fecha_ultimo_envio DESC)
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracion (
                    clave TEXT PRIMARY KEY,
                    valor TEXT
                )
            ''')

    def es_elegible_envio(self, correo: str, dias_espera: int) -> bool:
        """Verifica si un correo es elegible para envio."""
        if dias_espera <= 0:
            return True

        with self.get_cursor() as cursor:
            cursor.execute('''
                SELECT fecha_ultimo_envio FROM envios
                WHERE correo = ?
                ORDER BY fecha_ultimo_envio DESC LIMIT 1
            ''', (correo.lower(),))
            res = cursor.fetchone()

            if not res:
                return True

            fecha_ultimo = datetime.strptime(res[0], "%Y-%m-%d %H:%M:%S")
            return datetime.now() > (fecha_ultimo + timedelta(days=dias_espera))

    def registrar_envio(self, correo: str, plantilla: str):
        """Registra un envio exitoso."""
        with self.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO envios (correo, fecha_ultimo_envio, plantilla)
                VALUES (?, ?, ?)
            ''', (correo.lower(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), plantilla))

    def get_stats(self) -> dict:
        """Retorna estadisticas de la base de datos."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM envios")
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT correo) FROM envios")
            contactos = cursor.fetchone()[0]
            return {'total_envios': total, 'contactos_unicos': contactos}
```

---

### 4.4 Hash Seguro para Email Tracking

```python
import hashlib
import uuid

def generate_email_hash(email: str) -> str:
    """Genera un hash seguro del email para tracking."""
    # Opcion 1: SHA-256 (mas seguro)
    return hashlib.sha256(email.lower().encode('utf-8')).hexdigest()[:16]

    # Opcion 2: UUID v5 (deterministico y estandar)
    # NAMESPACE = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # DNS namespace
    # return str(uuid.uuid5(NAMESPACE, email.lower()))
```

---

### 4.5 Manejo de Excepciones Mejorado

```python
import logging
import traceback

def enviar_correo(self, nombre: str, email_destinatario: str, archivo_html_nombre: str) -> bool:
    """Envia un correo electronico.

    Args:
        nombre: Nombre del destinatario
        email_destinatario: Direccion de correo del destinatario
        archivo_html_nombre: Nombre del archivo de plantilla HTML

    Returns:
        bool: True si el envio fue exitoso, False en caso contrario

    Raises:
        ValueError: Si los parametros son invalidos
        FileNotFoundError: Si la plantilla no existe
    """
    # Validaciones
    if not nombre or not nombre.strip():
        self.log_msg("Error: Nombre de destinatario vacio", "ERROR")
        return False

    if not self.verificar_formato(email_destinatario):
        self.log_msg(f"Error: Email invalido: {email_destinatario}", "ERROR")
        return False

    try:
        # ... logica de envio ...

        context = ssl.create_default_context()
        # NO desactivar verificacion SSL
        # context.check_hostname = False  # ELIMINAR
        # context.verify_mode = ssl.CERT_NONE  # ELIMINAR

        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(remitente_email, remitente_pass)
            server.sendmail(remitente_email, email_destinatario, message.as_string())

        return True

    except smtplib.SMTPAuthenticationError as e:
        self.log_msg(f"Error de autenticacion SMTP: {e}", "ERROR")
        logging.error(f"SMTP Auth Error: {traceback.format_exc()}")
        return False
    except smtplib.SMTPException as e:
        self.log_msg(f"Error SMTP: {e}", "ERROR")
        logging.error(f"SMTP Error: {traceback.format_exc()}")
        return False
    except FileNotFoundError as e:
        self.log_msg(f"Plantilla no encontrada: {archivo_html_nombre}", "ERROR")
        logging.error(f"Template not found: {traceback.format_exc()}")
        return False
    except Exception as e:
        self.log_msg(f"Error inesperado enviando a {email_destinatario}: {e}", "ERROR")
        logging.error(f"Unexpected error: {traceback.format_exc()}")
        return False
```

---

### 4.6 Escritura CSV Segura

```python
import csv

def escribir_log_csv(self, log_csv: str, nombre: str, correo: str,
                     plantilla: str, estado: str):
    """Escribe un registro en el CSV de forma segura."""
    with open(log_csv, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            nombre,
            correo,
            plantilla,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            estado
        ])
```

---

## 5. Checklist de Accion Inmediata

Antes de desplegar este aplicativo en produccion:

- [ ] Crear archivo `.env` con todas las credenciales
- [ ] Agregar `.env` a `.gitignore`
- [ ] Eliminar credenciales hardcodeadas del codigo
- [ ] Eliminar las lineas que desactivan SSL
- [ ] Rotar todas las contrasenas expuestas en el historial de git
- [ ] Implementar threading seguro para Tkinter
- [ ] Agregar validacion de archivos Excel
- [ ] Configurar logging con rotacion
- [ ] Agregar archivo `.env.example` para referencia

---

## 6. Conclusion

El aplicativo cumple con su funcion principal de envio masivo de correos, pero presenta **deficiencias criticas de seguridad** que deben corregirse antes de cualquier uso en produccion. La exposicion de credenciales y la desactivacion de SSL son vulnerabilidades graves que podrian resultar en acceso no autorizado a cuentas de correo corporativo.

Se recomienda priorizar la correccion de los problemas criticos de seguridad antes de continuar con mejoras de performance o refactoring arquitectonico.

---

**Generado por:** Agente Validador de Codigo
**Framework:** Claude Code App Validator