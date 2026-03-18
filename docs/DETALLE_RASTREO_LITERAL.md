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

## 3. Inventario de Plantillas Disponibles
Existen 30 plantillas activas (3 por aplicativo). Cada apertura dispara un evento `apertura_correo` con un valor de `ep.plantilla` único:

| Aplicativo | Versión | ID de Plantilla (`ep.plantilla`) | Campaña Asociada (`ep.campana`) |
| :--- | :--- | :--- | :--- |
| **CRM** | v1 | `v1_crm` | `campana_crm` |
| | v2 | `v2_crm` | `campana_crm` |
| | v3 | `v3_crm` | `campana_crm` |
| **Rankmi (HCM)** | v1 | `v1_hcm` | `campana_hcm` |
| | v2 | `v2_hcm` | `campana_hcm` |
| | v3 | `v3_hcm` | `campana_hcm` |
| **Nextflow** | v1 | `v1_nextflow` | `campana_nextflow` |
| | v2 | `v2_nextflow` | `campana_nextflow` |
| | v3 | `v3_nextflow` | `campana_nextflow` |
| **Partners Truck**| v1 | `v1_partnerstruck` | `campana_partnerstruck` |
| | v2 | `v2_partnerstruck` | `campana_partnerstruck` |
| | v3 | `v3_partnerstruck` | `campana_partnerstruck` |
| **Smart Dent** | v1 | `v1_smartdent` | `campana_smartdent` |
| | v2 | `v2_smartdent` | `campana_smartdent` |
| | v3 | `v3_smartdent` | `campana_smartdent` |
| **ERP** | v1 | `v1_erp` | `campana_erp` |
| | v2 | `v2_erp` | `campana_erp` |
| | v3 | `v3_erp` | `campana_erp` |
| **Kardex** | v1 | `v1_kardex`# Plan de Acción: Auditoría Exhaustiva de UTMs

Este plan detalla la creación de un listado literal y completo de cada uno de los enlaces de rastreo generados para las 30 plantillas de la campaña Infrasys, utilizando el estándar de Google Analytics 4 (UTMs).

## Proposed Changes

### 1. [MODIFICAR] Documentación Técnica Literal
Actualizaremos el documento maestro de auditoría para que no sea solo una guía de "lógica", sino un listado real de todos los valores posibles.

#### [MODIFY] docs/DETALLE_RASTREO_LITERAL.md
- **Contenido Exhaustivo:** Listaremos cada aplicativo (CRM, HCM, ERP, etc.) y sus versiones (v1, v2, v3).
- **Desglose de Enlaces:** Para cada plantilla, listaremos literalmente los 11 tipos de `utm_content` que el script puede generar.
- **Formato:** Utilizaremos un formato de tabla o lista multinivel clara para que el usuario pueda copiar y pegar cualquier valor en los filtros de GA4.

## User Review Required

> [!NOTE]
> **Extensión del Documento**
> El listado final contendrá aproximadamente 330 entradas técnicas (30 plantillas x 11 tipos de enlace). Confirmar si el usuario prefiere este listado en un solo documento largo o dividido por aplicativos.

## Verification Plan

### Manual Verification
- Revisaremos que los 330 valores técnicos coincidan exactamente con la lógica programada en `update_tracking_tags.py`.
- Validaremos que el formato sea legible y fácil de navegar. Inyectado:**
`https://[DESTINO]?utm_source=partnertech&utm_medium=correo&utm_campaign=[CAMPANA]&utm_content=[PLANTILLA]_[ELEMENTO]&utm_term={{Email_Hash}}`

---
Última actualización: 18 de marzo de 2026. (Reporte de Auditoría Final)
