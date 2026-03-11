# Partner Tech | Gestor de Envío Masivo 🚀

Una aplicación de escritorio profesional desarrollada en Python para la gestión y automatización de campañas de correo electrónico masivo, optimizada para **Partner Tech**.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-blue?style=for-the-badge)
![GA4](https://img.shields.io/badge/Analytics-GA4-orange?style=for-the-badge&logo=google-analytics&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

## 🌟 Características Principales

- **👤 Gestión de Perfiles Multi-Remitente:** Permite alternar fácilmente entre diferentes cuentas de remitente (ej. Gerencia Comercial, Sub-Gerencia) con firmas y cargos automatizados.
- **📈 Rastreo Profesional (GA4):** Integración completa con Google Analytics 4 para medir:
  - **Aperturas de correo:** Mediante Measurement Protocol (píxel invisible).
  - **Clics en enlaces:** Parametrización automática con etiquetas UTM (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`).
  - **Atribución por plantilla:** Identificación de qué versión del correo generó la interacción.
- **🔒 Privacidad y Cumplimiento (PII):** Generación automática de **Hashes MD5** únicos para el `Client ID` de GA4, evitando el envío de correos electrónicos en texto plano a los servidores de Google.
- **📄 Plantillas HTML Robustas:** 6 versiones optimizadas para la campaña Infrasys, con diseño basado en tablas para máxima compatibilidad (Outlook, móviles) y fondo blanco corporativo.
- **👁️ Vista Previa en Tiempo Real:** Renderizado interactivo de las plantillas antes del envío para asegurar la calidad visual.
- **📊 Integración con Excel:** Carga masiva de destinatarios desde archivos `.xlsx` o `.xls`.
- **🛡️ Sistema Anti-Spam Inteligente:** 
  - Pausas automáticas entre correos (10-15 segundos aleatorios).
  - Pausas largas por lotes (cada 50 correos) para proteger la reputación del dominio.

## 🛠️ Requisitos Técnicos

- **Python 3.8 o superior**
- Dependencias listadas en `requirements.txt`:
  - `pandas`: Procesamiento de datos Excel.
  - `email-validator`: Validación de sintaxis de correos.
  - `tkinterweb`: Visualización de plantillas HTML en la interfaz.
  - `openpyxl`: Motor para lectura de archivos Excel modernos.
  - `hashlib`: (Nativo) Para la anonimización de datos de rastreo.

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

## 📁 Campañas y Plantillas Disponibles

Actualmente el sistema cuenta con 6 variantes estratégicas para la campaña **Infrasys**:
1. `correo_infrasys_v1_excel.html`: Enfoque en control de inventarios.
2. `correo_infrasys_v2_visibilidad.html`: Enfoque en visibilidad del negocio.
3. `correo_infrasys_v3_presupuestos.html`: Enfoque en control de presupuestos.
4. `correo_infrasys_v4_narrativa.html`: Enfoque narrativo y storytelling.
5. `correo_infrasys_v5_corto.html`: Versión minimalista y rápida.
6. `correo_infrasys_v6_directo.html`: Enfoque directo tipo "ventas".

## 📖 Guía de Uso

1. **Preparar Destinatarios:** Crea un Excel con las columnas exactas: `nombre` y `correo`.
2. **Seleccionar Remitente:** Escoge el perfil adecuado en el panel de configuración.
3. **Cargar Plantilla:** Selecciona una de las 6 versiones de Infrasys.
4. **Validar y Enviar:** Revisa la vista previa (los UTMs y Hash se generan automáticamente), carga el Excel y presiona **🚀 INICIAR ENVÍO**.

---

> [!IMPORTANT]
> **Aviso de Privacidad y GA4**: El sistema utiliza el ID de medición `G-FLPG7XG57W`. Para cumplir con las políticas de Google, el correo del destinatario se convierte en un hash antes de enviarse como `cid`. No modifique la lógica de `hashlib` en `main.py` para asegurar que nunca se envíen datos personales (PII) a Analytics.

Desarrollado para **Partner Tech** | 2026
