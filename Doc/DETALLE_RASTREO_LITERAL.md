# Auditoría de Parámetros de Rastreo - Campaña Infrasys 📊

Este documento contiene la lista exhaustiva de todos los valores de rastreo utilizados en los sistemas de envío y en las plantillas HTML de la campaña Infrasys.

## 1. Configuración Global
*   **ID de Medición (GA4):** `G-FLPG7XG57W`
*   **Protocolo de Google:** `v=2` (vía Google Analytics Measurement Protocol)

## 2. Rastreo de Apertura (Píxel de Medición)
El píxel de rastreo está ubicado al final de cada correo. Los parámetros fijos enviados en cada apertura son:

| Parámetro | Valor Literal | Descripción |
| :--- | :--- | :--- |
| `tid` | `G-FLPG7XG57W` | ID de la propiedad GA4 |
| `en` | `apertura_correo` | Nombre del evento registrado |
| `ep.campana` | `campana_infrasys` | Identificador de campaña |
| `cid` | `{{Email_Hash}}` | ID de cliente (Hash MD5 anónimo) |

### Valores de Plantilla (`ep.plantilla`) por Versión:
1.  **Versión Excel / Control:** `v1_excel`
2.  **Versión Visibilidad:** `v2_visibilidad`
3.  **Versión Presupuestos:** `v3_presupuestos`
4.  **Versión Narrativa:** `v4_narrativa`
5.  **Versión Corto:** `v5_corto`
6.  **Versión Directo:** `v6_directo`

## 3. Rastreo de Clics (Etiquetas UTM)
Todos los enlaces incluyen los siguientes parámetros para el análisis de tráfico:

*   **utm_source:** `partnertech`
*   **utm_medium:** `correo`
*   **utm_campaign:** `campana_infrasys`
*   **utm_term:** `{{Email_Hash}}` (Identificador MD5 del usuario)

### Valores de Contenido (`utm_content`) por Enlace Específico:

| Versión | Enlace / Botón | Valor Literal `utm_content` |
| :--- | :--- | :--- |
| **v1_excel** | Botón Agendar | `v1_excel_boton_agendar` |
| **v1_excel** | Enlace Sitio Web | `v1_excel_enlace_web` |
| **v2_visibilidad** | Botón Agendar | `v2_visibilidad_boton_agendar` |
| **v2_visibilidad** | Enlace Sitio Web | `v2_visibilidad_enlace_web` |
| **v3_presupuestos**| Botón Agendar | `v3_presupuestos_boton_agendar` |
| **v3_presupuestos**| Enlace Sitio Web | `v3_presupuestos_enlace_web` |
| **v4_narrativa** | Botón Agendar | `v4_narrativa_boton_agendar` |
| **v4_narrativa** | Enlace Sitio Web | `v4_narrativa_enlace_web` |
| **v5_corto** | Botón Agendar | `v5_corto_boton_agendar` |
| **v5_corto** | Enlace Sitio Web | `v5_corto_enlace_web` |
| **v6_directo** | Botón Agendar | `v6_directo_boton_agendar` |
| **v6_directo** | Enlace Sitio Web | `v6_directo_enlace_web` |

## 4. Hash de Identidad
*   **Algoritmo utilizado:** `MD5` (a través de la librería `hashlib` en `main.py`).
*   **Propósito:** Generar el valor para `cid` (píxel) y `utm_term` (clics) para permitir la trazabilidad individual en GA4 de forma anónima, sin enviar el correo en texto plano.

---
Última actualización: 11 de marzo de 2026.
