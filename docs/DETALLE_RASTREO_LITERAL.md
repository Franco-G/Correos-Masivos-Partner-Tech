# Auditoría de Parámetros de Rastreo - Campaña Partner Tech 📊

Este documento es el listado literal y veraz de todos los valores de rastreo presentes en las 30 plantillas HTML de la campaña.

## 1. Configuración Global
*   **ID de Medición (GA4):** `G-FLPG7XG57W`
*   **Protocolo de Google:** `v=2`
*   **Rastreo:** UTMs estándar de Google Analytics.

## 2. Rastreo de Apertura (Píxel)
Evento: `apertura_correo`
Parámetros fijos: `tid=G-FLPG7XG57W`, `v=2`, `en=apertura_correo`, `cid={{Email_Hash}}`.

## 3. Inventario de Plantillas (`apertura_correo`)

| Aplicativo | Plantilla (`ep.plantilla`) | Campaña (`ep.campana`) |
| :--- | :--- | :--- |
| **CRM** | `v1_crm`, `v2_crm`, `v3_crm` | `campana_crm` |
| **HCM** | `v1_hcm`, `v2_hcm`, `v3_hcm` | `campana_hcm` |
| **Nextflow** | `v1_nextflow`, `v2_nextflow`, `v3_nextflow` | `campana_nextflow` |
| **Partners Truck**| `v1_partnerstruck`, `v2_partnerstruck`, `v3_partnerstruck` | `campana_partnerstruck` |
| **Smart Dent** | `v1_smartdent`, `v2_smartdent`, `v3_smartdent` | `campana_smartdent` |
| **ERP** | `v1_erp`, `v2_erp`, `v3_erp` | `campana_erp` |
| **Kardex** | `v1_kardex`, `v2_kardex`, `v3_kardex` | `campana_kardex` |
| **GEMP** | `v1_gem`, `v2_gem`, `v3_gem` | `campana_gem` |
| **Clinic Mentor** | `v1_mentor`, `v2_mentor`, `v3_mentor` | `campana_mentor` |
| **Infrasys** | `v1_infrasys`, `v2_infrasys`, `v3_infrasys` | `campana_infrasys` |

---

## 4. Auditoría Exhaustiva de Clics (UTM)
A continuación se detallan los únicos 8 valores de `utm_content` que existen por cada plantilla. **TikTok y YouTube han sido eliminados por no estar presentes en el diseño original.**

### Estructura de sufijos por plantilla:
Para cualquier plantilla (ej: `v1_crm`), los enlaces son:
1.  `[ID]_boton_principal`: Botón CTA principal de la campaña.
2.  `[ID]_red_facebook`: Icono de Facebook en el pie.
3.  `[ID]_red_instagram`: Icono de Instagram en el pie.
4.  `[ID]_red_linkedin`: Icono de LinkedIn en el pie.
5.  `[ID]_boton_whatsapp`: Botón verde de contacto en la firma.
6.  `[ID]_enlace_web`: Link a `partnertech.pe` en la firma.
7.  `[ID]_enlace_correo`: Correo del remitente en la firma.
8.  `[ID]_enlace_remover`: Link para darse de baja en el pie legal.

### Listado Literal de `utm_content` (Auditado):

| ID Plantilla | Enlace Principal | Redes Sociales (FB/IG/LI) | Otros (WA/Web/Mail/Baja) |
| :--- | :--- | :--- | :--- |
| **v1_crm** | `v1_crm_boton_principal` | `v1_crm_red_facebook`, `v1_crm_red_instagram`, `v1_crm_red_linkedin` | `v1_crm_boton_whatsapp`, `v1_crm_enlace_web`, `v1_crm_enlace_correo`, `v1_crm_enlace_remover` |
| **v2_crm** | `v2_crm_boton_principal` | `v2_crm_red_facebook`, `v2_crm_red_instagram`, `v2_crm_red_linkedin` | `v2_crm_boton_whatsapp`, `v2_crm_enlace_web`, `v2_crm_enlace_correo`, `v2_crm_enlace_remover` |
| **v3_crm** | `v3_crm_boton_principal` | `v3_crm_red_facebook`, `v3_crm_red_instagram`, `v3_crm_red_linkedin` | `v3_crm_boton_whatsapp`, `v3_crm_enlace_web`, `v3_crm_enlace_correo`, `v3_crm_enlace_remover` |
| **v1_hcm** | `v1_hcm_boton_principal` | `v1_hcm_red_facebook`, `v1_hcm_red_instagram`, `v1_hcm_red_linkedin` | `v1_hcm_boton_whatsapp`, `v1_hcm_enlace_web`, `v1_hcm_enlace_correo`, `v1_hcm_enlace_remover` |
| **v2_hcm** | `v2_hcm_boton_principal` | `v2_hcm_red_facebook`, `v2_hcm_red_instagram`, `v2_hcm_red_linkedin` | `v2_hcm_boton_whatsapp`, `v2_hcm_enlace_web`, `v2_hcm_enlace_correo`, `v2_hcm_enlace_remover` |
| **v3_hcm** | `v3_hcm_boton_principal` | `v3_hcm_red_facebook`, `v3_hcm_red_instagram`, `v3_hcm_red_linkedin` | `v3_hcm_boton_whatsapp`, `v3_hcm_enlace_web`, `v3_hcm_enlace_correo`, `v3_hcm_enlace_remover` |
| **v1_nextflow** | `v1_nextflow_boton_principal` | `v1_nextflow_red_facebook`, `v1_nextflow_red_instagram`, `v1_nextflow_red_linkedin` | `v1_nextflow_boton_whatsapp`, `v1_nextflow_enlace_web`, `v1_nextflow_enlace_correo`, `v1_nextflow_enlace_remover` |
| **v2_nextflow** | `v2_nextflow_boton_principal` | `v2_nextflow_red_facebook`, `v2_nextflow_red_instagram`, `v2_nextflow_red_linkedin` | `v2_nextflow_boton_whatsapp`, `v2_nextflow_enlace_web`, `v2_nextflow_enlace_correo`, `v2_nextflow_enlace_remover` |
| **v3_nextflow** | `v3_nextflow_boton_principal` | `v3_nextflow_red_facebook`, `v3_nextflow_red_instagram`, `v3_nextflow_red_linkedin` | `v3_nextflow_boton_whatsapp`, `v3_nextflow_enlace_web`, `v3_nextflow_enlace_correo`, `v3_nextflow_enlace_remover` |
| **v1_partnerstruck** | `v1_partnerstruck_boton_principal` | `v1_partnerstruck_red_facebook`, `v1_partnerstruck_red_instagram`, `v1_partnerstruck_red_linkedin` | `v1_partnerstruck_boton_whatsapp`, `v1_partnerstruck_enlace_web`, `v1_partnerstruck_enlace_correo`, `v1_partnerstruck_enlace_remover` |
| **v2_partnerstruck** | `v2_partnerstruck_boton_principal` | `v2_partnerstruck_red_facebook`, `v2_partnerstruck_red_instagram`, `v2_partnerstruck_red_linkedin` | `v2_partnerstruck_boton_whatsapp`, `v2_partnerstruck_enlace_web`, `v2_partnerstruck_enlace_correo`, `v2_partnerstruck_enlace_remover` |
| **v3_partnerstruck** | `v3_partnerstruck_boton_principal` | `v3_partnerstruck_red_facebook`, `v3_partnerstruck_red_instagram`, `v3_partnerstruck_red_linkedin` | `v3_partnerstruck_boton_whatsapp`, `v3_partnerstruck_enlace_web`, `v3_partnerstruck_enlace_correo`, `v3_partnerstruck_enlace_remover` |
| **v1_smartdent** | `v1_smartdent_boton_principal` | `v1_smartdent_red_facebook`, `v1_smartdent_red_instagram`, `v1_smartdent_red_linkedin` | `v1_smartdent_boton_whatsapp`, `v1_smartdent_enlace_web`, `v1_smartdent_enlace_correo`, `v1_smartdent_enlace_remover` |
| **v2_smartdent** | `v2_smartdent_boton_principal` | `v2_smartdent_red_facebook`, `v2_smartdent_red_instagram`, `v2_smartdent_red_linkedin` | `v2_smartdent_boton_whatsapp`, `v2_smartdent_enlace_web`, `v2_smartdent_enlace_correo`, `v2_smartdent_enlace_remover` |
| **v3_smartdent** | `v3_smartdent_boton_principal` | `v3_smartdent_red_facebook`, `v3_smartdent_red_instagram`, `v3_smartdent_red_linkedin` | `v3_smartdent_boton_whatsapp`, `v3_smartdent_enlace_web`, `v3_smartdent_enlace_correo`, `v3_smartdent_enlace_remover` |
| **v1_erp** | `v1_erp_boton_principal` | `v1_erp_red_facebook`, `v1_erp_red_instagram`, `v1_erp_red_linkedin` | `v1_erp_boton_whatsapp`, `v1_erp_enlace_web`, `v1_erp_enlace_correo`, `v1_erp_enlace_remover` |
| **v2_erp** | `v2_erp_boton_principal` | `v2_erp_red_facebook`, `v2_erp_red_instagram`, `v2_erp_red_linkedin` | `v2_erp_boton_whatsapp`, `v2_erp_enlace_web`, `v2_erp_enlace_correo`, `v2_erp_enlace_remover` |
| **v3_erp** | `v3_erp_boton_principal` | `v3_erp_red_facebook`, `v3_erp_red_instagram`, `v3_erp_red_linkedin` | `v3_erp_boton_whatsapp`, `v3_erp_enlace_web`, `v3_erp_enlace_correo`, `v3_erp_enlace_remover` |
| **v1_kardex** | `v1_kardex_boton_principal` | `v1_kardex_red_facebook`, `v1_kardex_red_instagram`, `v1_kardex_red_linkedin` | `v1_kardex_boton_whatsapp`, `v1_kardex_enlace_web`, `v1_kardex_enlace_correo`, `v1_kardex_enlace_remover` |
| **v2_kardex** | `v2_kardex_boton_principal` | `v2_kardex_red_facebook`, `v2_kardex_red_instagram`, `v2_kardex_red_linkedin` | `v2_kardex_boton_whatsapp`, `v2_kardex_enlace_web`, `v2_kardex_enlace_correo`, `v2_kardex_enlace_remover` |
| **v3_kardex** | `v3_kardex_boton_principal` | `v3_kardex_red_facebook`, `v3_kardex_red_instagram`, `v3_kardex_red_linkedin` | `v3_kardex_boton_whatsapp`, `v3_kardex_enlace_web`, `v3_kardex_enlace_correo`, `v3_kardex_enlace_remover` |
| **v1_gem** | `v1_gem_boton_principal` | `v1_gem_red_facebook`, `v1_gem_red_instagram`, `v1_gem_red_linkedin` | `v1_gem_boton_whatsapp`, `v1_gem_enlace_web`, `v1_gem_enlace_correo`, `v1_gem_enlace_remover` |
| **v2_gem** | `v2_gem_boton_principal` | `v2_gem_red_facebook`, `v2_gem_red_instagram`, `v2_gem_red_linkedin` | `v2_gem_boton_whatsapp`, `v2_gem_enlace_web`, `v2_gem_enlace_correo`, `v2_gem_enlace_remover` |
| **v3_gem** | `v3_gem_boton_principal` | `v3_gem_red_facebook`, `v3_gem_red_instagram`, `v3_gem_red_linkedin` | `v3_gem_boton_whatsapp`, `v3_gem_enlace_web`, `v3_gem_enlace_correo`, `v3_gem_enlace_remover` |
| **v1_mentor** | `v1_mentor_boton_principal` | `v1_mentor_red_facebook`, `v1_mentor_red_instagram`, `v1_mentor_red_linkedin` | `v1_mentor_boton_whatsapp`, `v1_mentor_enlace_web`, `v1_mentor_enlace_correo`, `v1_mentor_enlace_remover` |
| **v2_mentor** | `v2_mentor_boton_principal` | `v2_mentor_red_facebook`, `v2_mentor_red_instagram`, `v2_mentor_red_linkedin` | `v2_mentor_boton_whatsapp`, `v2_mentor_enlace_web`, `v2_mentor_enlace_correo`, `v2_mentor_enlace_remover` |
| **v3_mentor** | `v3_mentor_boton_principal` | `v3_mentor_red_facebook`, `v3_mentor_red_instagram`, `v3_mentor_red_linkedin` | `v3_mentor_boton_whatsapp`, `v3_mentor_enlace_web`, `v3_mentor_enlace_correo`, `v3_mentor_enlace_remover` |
| **v1_infrasys** | `v1_infrasys_boton_principal` | `v1_infrasys_red_facebook`, `v1_infrasys_red_instagram`, `v1_infrasys_red_linkedin` | `v1_infrasys_boton_whatsapp`, `v1_infrasys_enlace_web`, `v1_infrasys_enlace_correo`, `v1_infrasys_enlace_remover` |
| **v2_infrasys** | `v2_infrasys_boton_principal` | `v2_infrasys_red_facebook`, `v2_infrasys_red_instagram`, `v2_infrasys_red_linkedin` | `v2_infrasys_boton_whatsapp`, `v2_infrasys_enlace_web`, `v2_infrasys_enlace_correo`, `v2_infrasys_enlace_remover` |
| **v3_infrasys** | `v3_infrasys_boton_principal` | `v3_infrasys_red_facebook`, `v3_infrasys_red_instagram`, `v3_infrasys_red_linkedin` | `v3_infrasys_boton_whatsapp`, `v3_infrasys_enlace_web`, `v3_infrasys_enlace_correo`, `v3_infrasys_enlace_remover` |

---

## 5. Guía de Uso en GA4
1.  **Apertura**: Usa los parámetros `ep.plantilla` y `ep.campana` del evento `apertura_correo`.
2.  **Clics**: 
    *   **Campaña**: La dimensión "**Nombre de campaña manual de la sesión**" corresponde al parámetro `utm_campaign`. Su valor es exactamente el mismo listado como "Campaña (`ep.campana`)" en la tabla de la Sección 3 (ej: `campana_crm`, `campana_hcm`, etc.).
    *   **Enlace Específico**: La dimensión "**Contenido de anuncio manual de la sesión**" corresponde a `utm_content`. Úsala para filtrar por los valores listados en la Sección 4 (ej: Filtrar por `contiene "boton_whatsapp"` para ver efectividad del botón verde de contacto).

---
Última actualización: 18 de marzo de 2026. (Reporte Maestro Consolidado y Limpio)
