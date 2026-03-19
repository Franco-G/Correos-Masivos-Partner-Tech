# 📊 Estrategia Final de Trazabilidad GA4: Inventario Máster Diferenciado

Este documento representa el inventario atómico definitivo de todos los puntos de rastreo de la campaña Partner Tech. Refleja la inyección técnica exacta en los correos y cómo se leerá en Google Analytics, garantizando la **diferenciación total por aplicativo y versión** en cada clic.

---

## 🏗️ Tabla 1: Jerarquía de Eventos Custom (Píxel de Apertura)
Rastro interno del píxel de apertura agrupado por parámetro.

| Nombre del evento (en) | Parámetro de evento (ep) | Valor Literal (valor técnico) |
| :--- | :--- | :--- |
| **apertura_correo** | `campana` | `campana_mentor`, `campana_crm`, `campana_erp`, `campana_gem`, `campana_hcm`, `campana_infrasys`, `campana_kardex`, `campana_nextflow`, `campana_partnerstruck`, `campana_smartdent` |
| **apertura_correo** | `plantilla` | `v1_mentor`, `v2_mentor`, `v3_mentor`, `v1_crm`, `v2_crm`, `v3_crm`, `v1_erp`, `v2_erp`, `v3_erp`, `v1_gem`, `v2_gem`, `v3_gem`, `v1_hcm`, `v2_hcm`, `v3_hcm`, `v1_infrasys`, `v2_infrasys`, `v3_infrasys`, `v1_kardex`, `v2_kardex`, `v3_kardex`, `v1_nextflow`, `v2_nextflow`, `v3_nextflow`, `v1_partnerstruck`, `v2_partnerstruck`, `v3_partnerstruck`, `v1_smartdent`, `v2_smartdent`, `v3_smartdent` |

---

## 🔗 Tabla 2: Jerarquía de Enlaces UTM (Clics Diferenciados 1:1)
Mapeo exhaustivo donde el **Contenido del Anuncio (`utm_content`) viaja con el prefijo exacto de su versión y aplicativo**, lo que te permite en Analytics desglosar el rendimiento átomo por átomo desde un solo reporte.

| Campaña de la sesión (utm_campaign) | Contenido del anuncio manual (utm_content) |
| :--- | :--- |
| `campana_crm` | `v1_crm_boton_cta`, `v2_crm_boton_cta`, `v3_crm_boton_cta`, `v1_crm_boton_whatsapp`, `v2_crm_boton_whatsapp`, `v3_crm_boton_whatsapp`, `v1_crm_enlace_correo_emisor`, `v2_crm_enlace_correo_emisor`, `v3_crm_enlace_correo_emisor`, `v1_crm_enlace_correo_empresa`, `v2_crm_enlace_correo_empresa`, `v3_crm_enlace_correo_empresa` |
| `campana_hcm` | `v1_hcm_boton_cta`, `v2_hcm_boton_cta`, `v3_hcm_boton_cta`, `v1_hcm_boton_whatsapp`, `v2_hcm_boton_whatsapp`, `v3_hcm_boton_whatsapp`, `v1_hcm_enlace_correo_emisor`, `v2_hcm_enlace_correo_emisor`, `v3_hcm_enlace_correo_emisor`, `v1_hcm_enlace_correo_empresa`, `v2_hcm_enlace_correo_empresa`, `v3_hcm_enlace_correo_empresa` |
| `campana_erp` | `v1_erp_boton_cta`, `v2_erp_boton_cta`, `v3_erp_boton_cta`, `v1_erp_boton_whatsapp`, `v2_erp_boton_whatsapp`, `v3_erp_boton_whatsapp`, `v1_erp_enlace_correo_emisor`, `v2_erp_enlace_correo_emisor`, `v3_erp_enlace_correo_emisor`, `v1_erp_enlace_correo_empresa`, `v2_erp_enlace_correo_empresa`, `v3_erp_enlace_correo_empresa` |
| `campana_gem` | `v1_gem_boton_cta`, `v2_gem_boton_cta`, `v3_gem_boton_cta`, `v1_gem_boton_whatsapp`, `v2_gem_boton_whatsapp`, `v3_gem_boton_whatsapp`, `v1_gem_enlace_correo_emisor`, `v2_gem_enlace_correo_emisor`, `v3_gem_enlace_correo_emisor`, `v1_gem_enlace_correo_empresa`, `v2_gem_enlace_correo_empresa`, `v3_gem_enlace_correo_empresa` |
| `campana_mentor` | `v1_mentor_boton_cta`, `v2_mentor_boton_cta`, `v3_mentor_boton_cta`, `v1_mentor_boton_whatsapp`, `v2_mentor_boton_whatsapp`, `v3_mentor_boton_whatsapp`, `v1_mentor_enlace_correo_emisor`, `v2_mentor_enlace_correo_emisor`, `v3_mentor_enlace_correo_emisor`, `v1_mentor_enlace_correo_empresa`, `v2_mentor_enlace_correo_empresa`, `v3_mentor_enlace_correo_empresa` |
| `campana_infrasys` | `v1_infrasys_boton_cta`, `v2_infrasys_boton_cta`, `v3_infrasys_boton_cta`, `v1_infrasys_boton_whatsapp`, `v2_infrasys_boton_whatsapp`, `v3_infrasys_boton_whatsapp`, `v1_infrasys_enlace_correo_emisor`, `v2_infrasys_enlace_correo_emisor`, `v3_infrasys_enlace_correo_emisor`, `v1_infrasys_enlace_correo_empresa`, `v2_infrasys_enlace_correo_empresa`, `v3_infrasys_enlace_correo_empresa` |
| `campana_kardex` | `v1_kardex_boton_cta`, `v2_kardex_boton_cta`, `v3_kardex_boton_cta`, `v1_kardex_boton_whatsapp`, `v2_kardex_boton_whatsapp`, `v3_kardex_boton_whatsapp`, `v1_kardex_enlace_correo_emisor`, `v2_kardex_enlace_correo_emisor`, `v3_kardex_enlace_correo_emisor`, `v1_kardex_enlace_correo_empresa`, `v2_kardex_enlace_correo_empresa`, `v3_kardex_enlace_correo_empresa` |
| `campana_nextflow` | `v1_nextflow_boton_cta`, `v2_nextflow_boton_cta`, `v3_nextflow_boton_cta`, `v1_nextflow_boton_whatsapp`, `v2_nextflow_boton_whatsapp`, `v3_nextflow_boton_whatsapp`, `v1_nextflow_enlace_correo_emisor`, `v2_nextflow_enlace_correo_emisor`, `v3_nextflow_enlace_correo_emisor`, `v1_nextflow_enlace_correo_empresa`, `v2_nextflow_enlace_correo_empresa`, `v3_nextflow_enlace_correo_empresa` |
| `campana_partnerstruck` | `v1_partnerstruck_boton_cta`, `v2_partnerstruck_boton_cta`, `v3_partnerstruck_boton_cta`, `v1_partnerstruck_boton_whatsapp`, `v2_partnerstruck_boton_whatsapp`, `v3_partnerstruck_boton_whatsapp`, `v1_partnerstruck_enlace_correo_emisor`, `v2_partnerstruck_enlace_correo_emisor`, `v3_partnerstruck_enlace_correo_emisor`, `v1_partnerstruck_enlace_correo_empresa`, `v2_partnerstruck_enlace_correo_empresa`, `v3_partnerstruck_enlace_correo_empresa` |
| `campana_smartdent` | `v1_smartdent_boton_cta`, `v2_smartdent_boton_cta`, `v3_smartdent_boton_cta`, `v1_smartdent_boton_whatsapp`, `v2_smartdent_boton_whatsapp`, `v3_smartdent_boton_whatsapp`, `v1_smartdent_enlace_correo_emisor`, `v2_smartdent_enlace_correo_emisor`, `v3_smartdent_enlace_correo_emisor`, `v1_smartdent_enlace_correo_empresa`, `v2_smartdent_enlace_correo_empresa`, `v3_smartdent_enlace_correo_empresa` |
| `redes_sociales` | `red_facebook`, `red_instagram`, `red_linkedin` *(Universales cruzados globalmente)* |
| `sitio_web` | `enlace_web` |
| `legal` | `enlace_remover` |

---

## 📚 Definición para Auditoría en GA4
1.  **Píxel (Tabla 1)**: Filtra por el evento `apertura_correo` y desglosa por `campana` y `plantilla`.
2.  **Clics (Tabla 2)**: Al visualizar el reporte de clics, la dimensión de contenido (`utm_content`) ahora es explicita y cuenta una historia completa: *Ej: Sé que este clic exacto vino del botón CTA de la versión 1 del CRM (`v1_crm_boton_cta`)* eliminando así la ambigüedad en la atribución.

---
*Última actualización: 18 de marzo de 2026. (Reporte Integral Suprema Literal GA4 Diferenciada).*
