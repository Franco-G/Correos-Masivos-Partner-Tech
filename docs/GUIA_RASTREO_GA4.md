# Parámetros Exactos de Rastreo - Campaña Partner Tech 📈

Este documento detalla los valores **literales** configurados en el sistema y las plantillas. Estos son los términos exactos que verás al analizar los datos en el panel de **Google Analytics 4**.

## 1. Configuración de la Propiedad
*   **ID de Medición (`tid`):** `G-FLPG7XG57W`

## 2. Rastreo de Aperturas (Píxel Invisible)
Busca estos datos en tus reportes de eventos:

| Parámetro / Campo | Valor Literal | ¿Para qué sirve? |
| :--- | :--- | :--- |
| **Nombre del Evento (`en`)** | `apertura_correo` | Filtro principal para ver quién abrió correos. |
| **Campaña (`ep.campana`)** | `campana_infrasys`, `campana_crm`, `campana_hcm`, `campana_nextflow`, `campana_truck`, `campana_smartdent`, `campana_erp`, `campana_kardex`, `campana_gem`, `campana_clinic` | Agrupa todas las aperturas de la campaña respectiva. |
| **Plantilla (`ep.plantilla`)** | Ej: `v1_crm`, `v2_hcm`, `v3_erp`, `v4_partnerstruck` | Identifica qué diseño específico fue abierto. |
| **ID de Usuario (`cid`)** | `[HASH_MD5]` | Identificador anónimo del cliente. |

## 3. Rastreo de Clics (Etiquetas UTM)
Datos registrados cuando el cliente interactúa con los botones o enlaces:

| Etiqueta UTM | Valor Literal | Función |
| :--- | :--- | :--- |
| **Fuente (`utm_source`)** | `partnertech` | Origen del tráfico. |
| **Medio (`utm_medium`)** | `correo` | Clasificación del tráfico. |
| **Campaña (`utm_campaign`)** | Ej: `campana_{app}`, `correo_empresa`, `redes_sociales`, `sitio_web`, `legal` | Agrupa el tráfico por campaña de producto o un canal global. |
| **Contenido (`utm_content`)** | Ej: `{plantilla}_boton_cta`, `{plantilla}_boton_whatsapp`, `{plantilla}_enlace_correo_emisor`, `enlace_correo_empresa` | Segmentación estricta para saber qué elemento interactivo se presionó, vinculado a un diseño o global. |
| **Término (`utm_term`)** | `[HASH_MD5]` | ID anónimo del cliente que hizo clic, inyectado por `main.py`. |

---

## 4. 🛠️ Configuración de Informes en GA4 (Pasos a seguir)

Para poder visualizar correctamente la información anterior, debes realizar estas configuraciones en tu panel:

### Paso A: Registrar Dimensiones Personalizadas (Obligatorio)
Para que GA4 reconozca los datos del píxel de apertura (como el nombre de la plantilla), haz esto:
1. Ve a **Administrar** (icono de engranaje ⚙️) > **Visualización de datos** > **Definiciones personalizadas**.
2. Haz clic en **Crear dimensiones personalizadas**.
3. Registra las siguientes:
   *   **Nombre**: `Plantilla` | **Ámbito**: Evento | **Parámetro**: `plantilla`
   *   **Nombre**: `Campaña Email` | **Ámbito**: Evento | **Parámetro**: `campana`

### Paso B: Configurar Reporte de Clics (UTMs)
1. Ve a **Informes** > **Adquisición** > **Adquisición de tráfico**.
2. En la tabla, selecciona como dimensión principal **Fuente/medio de la sesión** (verás `partnertech / correo`).
3. Haz clic en el botón **"+"** azul al lado de la columna actual y busca **"Contenido del anuncio manual"**.
4. Ahora verás los valores tipo `v1_crm_boton_cta`, `v2_hcm_boton_whatsapp` o `enlace_correo_empresa` junto al tráfico.

### Paso C: Crear Informe de Aperturas (Exploración)
1. Ve a **Explorar** > **Exploración en blanco**.
2. En **Dimensiones (+)** importa: `Nombre del evento` y `Plantilla`.
3. En **Métricas (+)** importa: `Número de eventos`.
4. Arrastra **Plantilla** a Filas y **Número de eventos** a Valores.
5. Aplica un Filtro: `Nombre del evento` coincide exactamente con `apertura_correo`.

---
**Hash MD5**: Generado automáticamente por el software a partir del email para asegurar la privacidad y cumplir con las leyes PII de Google.
