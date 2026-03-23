import pandas as pd
import email_validator
import tkinterweb
import openpyxl
from dotenv import load_dotenv

print("--- DIAGNÓSTICO DE ENTORNO ---")
import sys
print(f"Intérprete actual: {sys.executable}")
print(f"Rutas de búsqueda: {sys.path}")

try:
    print(f"Versión de Pandas: {pd.__version__}")
    print("Todas las librerías críticas cargadas correctamente.")
except Exception as e:
    print(f"Error al cargar librerías: {e}")
