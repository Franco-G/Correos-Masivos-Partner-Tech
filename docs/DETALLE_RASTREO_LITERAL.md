# 📊 Estrategia Final de Trazabilidad GA4: Inventario Máster Compacto

Este documento representa el inventario atómico definitivo de todos los puntos de rastreo de la campaña Partner Tech, reflejando exactamente lo que se verá en Google Analytics de forma estructurada.

---

## 🏗️ Tabla 1: Jerarquía de Eventos Custom (Píxel de Apertura)
Rastro interno del píxel de apertura agrupado por parámetro.

| en (Evento) | ep (Parámetro) | VALORES TÉCNICOS LITERALES (En Google Analytics) |
| :--- | :--- | :--- |
| **apertura_correo** | `campana` | `campana_mentor`, `campana_crm`, `campana_erp`, `campana_gem`, `campana_hcm`, `campana_infrasys`, `campana_kardex`, `campana_nextflow`, `campana_partnerstruck`, `campana_smartdent` |
| **apertura_correo** | `plantilla` | `v1_mentor`, `v2_mentor`, `v3_mentor`, `v1_crm`, `v2_crm`, `v3_crm`, `v1_erp`, `v2_erp`, `v3_erp`, `v1_gem`, `v2_gem`, `v3_gem`, `v1_hcm`, `v2_hcm`, `v3_hcm`, `v1_infrasys`, `v2_infrasys`, `v3_infrasys`, `v1_kardex`, `v2_kardex`, `v3_kardex`, `v1_nextflow`, `v2_nextflow`, `v3_nextflow`, `v1_partnerstruck`, `v2_partnerstruck`, `v3_partnerstruck`, `v1_smartdent`, `v2_smartdent`, `v3_smartdent` |

---

## 🔗 Tabla 2: Jerarquía de Enlaces UTM (Lo que verás en GA4 Clics)
Mapeo literal exacto de los valores que Google Analytics capturará en sus reportes para la dimensión "Contenido del Anuncio" (`utm_content`), agrupados por campaña.

| utm_campaign (Campaña) | utm_content (Valores Litérales Exactos en GA4) |
| :--- | :--- |
| `campana_crm` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_hcm` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_erp` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_gem` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_mentor` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_infrasys` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_kardex` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_nextflow` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_partnerstruck` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `campana_smartdent` | `boton_cta`, `boton_whatsapp`, `enlace_whatsapp`, `enlace_correo` |
| `redes_sociales` | `red_facebook`, `red_instagram`, `red_linkedin` |
| `sitio_web` | `enlace_web` |
| `legal` | `enlace_remover` |

---

## 📚 Definición para Auditoría en GA4
1.  **Píxel (Tabla 1)**: Para auditar aperturas, busca el evento `apertura_correo` y filtra por los parámetros personalizados `campana` y `plantilla`. **Aquí es donde sabes si el correo era v1, v2 o v3**.
2.  **Clics (Tabla 2)**: Para auditar clics, utiliza los informes de "Campaña" (`utm_campaign`) y desglosa usando el "Contenido del anuncio" (`utm_content`). **Todos los botones de las versiones v1, v2 y v3 de una campaña se agruparán bajo el mismo valor literal (ej. `boton_cta`), unificando el rendimiento por elemento.**

---
*Última actualización: 18 de marzo de 2026. (Reporte Integral Suprema Literal GA4).*
