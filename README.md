# Partner Tech | Gestor de Envío Masivo 🚀

Una aplicación de escritorio profesional desarrollada en Python para la gestión y automatización de campañas de correo electrónico masivo, optimizada para **Partner Tech**.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

## 🌟 Características Principales

- **👤 Gestión de Perfiles Multi-Remitente:** Permite alternar fácilmente entre diferentes cuentas de remitente (ej. Gerencia Comercial, Sub-Gerencia) con firmas y cargos automatizados.
- **📄 Plantillas HTML Dinámicas:** Soporte para plantillas personalizables con placeholders como `{{Nombre_Contacto}}`, `{{Nombre_Remitente}}`, etc.
- **👁️ Vista Previa en Tiempo Real:** Renderizado interactivo de las plantillas antes del envío para asegurar la calidad visual.
- **📊 Integración con Excel:** Carga masiva de destinatarios desde archivos `.xlsx` o `.xls`.
- **🛡️ Sistema Anti-Spam Inteligente:** 
  - Pausas automáticas entre correos (10-15 segundos aleatorios).
  - Pausas largas por lotes (cada 50 correos) para proteger la reputación del dominio.
- **📝 Registro y Trazabilidad:** Historial detallado de envíos exitosos y fallidos en formato CSV y LOG.
- **⚖️ Cumplimiento Normativo:** Estructura de correos alineada con los lineamientos de la **Cámara de Comercio de Lima (CCL)**, incluyendo opciones de baja (unsubscribe).

## 🛠️ Requisitos Técnicos

- **Python 3.8 o superior**
- Dependencias listadas en `requirements.txt`:
  - `pandas`: Procesamiento de datos Excel.
  - `email-validator`: Validación de sintaxis de correos.
  - `tkinterweb`: Visualización de plantillas HTML en la interfaz.
  - `openpyxl`: Motor para lectura de archivos Excel modernos.

## 🚀 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone [url-del-repositorio]
   cd correos-masivos-partner-tech
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración SMTP:**
   La aplicación utiliza los servidores de Partner Tech por defecto:
   - **Servidor:** `mail.partnertech.pe`
   - **Puerto:** `465` (SSL)

## 📖 Guía de Uso

1. **Preparar Destinatarios:** Crea un Excel con las columnas exactas: `nombre` y `correo`.
2. **Seleccionar Remitente:** Escoge el perfil adecuado en el panel de configuración.
3. **Cargar Plantilla:** Selecciona el archivo `.html` de la campaña.
4. **Validar y Enviar:** Revisa la vista previa, carga el Excel y presiona **🚀 INICIAR ENVÍO**.

## 📁 Estructura del Proyecto

- `main.py`: Núcleo de la aplicación y lógica de la interfaz.
- `correo_ejemplo.html`: Plantilla base para campañas.
- `registro_envios.csv`: Historial acumulado de actividad.
- `Logo_blanco_ver1.png`: Identidad visual de Partner Tech para los correos.

---

> [!IMPORTANT]
> **Aviso de Privacidad**: Esta herramienta debe usarse exclusivamente para comunicaciones corporativas autorizadas. Asegúrese de respetar las listas de exclusión de los clientes.

Desarrollado para **Partner Tech** | 2026
