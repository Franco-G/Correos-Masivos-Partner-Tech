# Partner Tech | Gestor de Envío Masivo 🚀

Este proyecto es una aplicación de escritorio desarrollada en **Python** diseñada para automatizar y gestionar el envío masivo de correos electrónicos corporativos de **Partner Tech**. La herramienta permite utilizar plantillas HTML personalizadas y listas de contactos gestionadas desde archivos Excel.

## ✨ Características Principales

- **Gestión de Perfiles**: Permite alternar entre diferentes perfiles de remitente (ej. Franco Guerrero, Alexandra Cardozo) configurando automáticamente el nombre, email, cargo y firma.
- **Editor Visual de Plantillas**: Incorpora un potente editor que permite crear y modificar plantillas HTML en tiempo real con bloques de contenido (títulos, párrafos, botones, beneficios).
- **Vista Previa Real**: Visualización inmediata de cómo se verá el correo antes de enviarlo, incluyendo el reemplazo dinámico de variables como `{{Nombre_Contacto}}`.
- **Soporte Multimedia**: Gestión automática de imágenes embebidas (logos) y archivos adjuntos (brochures).
- **Seguridad y Validación**: Validación de formatos de correo electrónico y conexión segura vía SMTP con SSL/TLS.
- **Registro Detallado**: Sistema de logging que genera un historial de envíos y errores en `registro_envios.log`.

## 🛠️ Requisitos e Instalación

### Requisitos Previos
- **Python 3.8+**
- Un servidor SMTP configurado (por defecto `mail.partnertech.pe`).

### Instalación de Dependencias

Clona el repositorio y ejecuta el siguiente comando para instalar las librerías necesarias:

```bash
pip install -r requirements.txt
```

Las dependencias principales son:
- `pandas` & `openpyxl`: Para el manejo de bases de datos en Excel.
- `email-validator`: Para validar la integridad de los correos de destino.
- `tkinterweb`: Para el motor de renderizado HTML dentro de la aplicación.

## 🚀 Guía de Uso

1. **Configuración de Datos**: Asegúrate de tener el archivo `Correos.xlsx` en la raíz con las columnas correspondientes (Nombre del contacto, Email, etc.).
2. **Ejecución**: Inicia la aplicación ejecutando:
   ```bash
   python main.py
   ```
3. **Selección de Remitente**: Elige tu perfil en el panel de configuración.
4. **Preparación del Correo**: Selecciona una plantilla HTML existente o crea una nueva en el "Editor de Plantillas".
5. **Envío**: Pulsa el botón **🚀 INICIAR ENVÍO**. Puedes monitorear el progreso en el panel de "Registro de Actividad".

## 📁 Estructura del Proyecto

```text
├── main.py                   # Código fuente principal (Lógica y UI)
├── requirements.txt          # Dependencias del proyecto
├── Correos.xlsx              # Base de datos de destinatarios (Excel)
├── Logo_blanco_ver1.png      # Logo corporativo para los correos
├── correo_*.html             # Plantillas de correo predefinidas
├── PartnerTechMailer.exe     # Ejecutable compilado para Windows
├── registro_envios.log       # Historial de actividades y errores
└── registro_envios.csv       # Registro estructurado de cada envío exitoso
```

---

*Desarrollado para la optimización de procesos comerciales de Partner Tech.*
