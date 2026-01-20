import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="partner_mailer.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de Historial de Envíos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS envios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_contacto TEXT,
                    email_destinatario TEXT,
                    plantilla TEXT,
                    fecha DATETIME,
                    estado TEXT,
                    error TEXT
                )
            ''')
            
            # Tabla de Plantillas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS plantillas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE,
                    contenido_html TEXT,
                    fecha_creacion DATETIME
                )
            ''')
            
            # Tabla de Perfiles de Remitente
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS perfiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE,
                    email TEXT,
                    password TEXT,
                    cargo TEXT
                )
            ''')
            
            conn.commit()

    def registrar_envio(self, nombre, email, plantilla, estado, error=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO envios (nombre_contacto, email_destinatario, plantilla, fecha, estado, error)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, email, plantilla, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), estado, error))
            conn.commit()

    def obtener_historial(self, limite=100):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nombre_contacto, email_destinatario, plantilla, fecha, estado FROM envios ORDER BY fecha DESC LIMIT ?', (limite,))
            return cursor.fetchall()

    def guardar_plantilla(self, nombre, html):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO plantillas (nombre, contenido_html, fecha_creacion)
                VALUES (?, ?, ?)
            ''', (nombre, html, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

    def obtener_plantillas(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nombre FROM plantillas ORDER BY nombre')
            return [r[0] for r in cursor.fetchall()]

    def obtener_contenido_plantilla(self, nombre):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT contenido_html FROM plantillas WHERE nombre = ?', (nombre,))
            res = cursor.fetchone()
            return res[0] if res else None

    def guardar_perfil(self, nombre, email, password, cargo):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO perfiles (nombre, email, password, cargo)
                VALUES (?, ?, ?, ?)
            ''', (nombre, email, password, cargo))
            conn.commit()

    def obtener_perfiles(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nombre, email, password, cargo FROM perfiles')
            return {r[0]: {"email": r[1], "pass": r[2], "cargo": r[3]} for r in cursor.fetchall()}
