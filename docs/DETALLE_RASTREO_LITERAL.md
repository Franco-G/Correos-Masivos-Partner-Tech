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

### Valores de Plantilla (`ep.plantilla`) por Aplicativo:

#### 1. CRM
1. `v1_crm`
2. `v2_crm`
3. `v3_crm`

#### 2. HCM (Rankmi)
1. `v1_hcm`
2. `v2_hcm`
3. `v3_hcm`

#### 3. NEXTFLOW (BPM)
1. `v1_nextflow`
2. `v2_nextflow`
3. `v3_nextflow`

#### 4. PARTNERS TRUCK
1. `v1_partnerstruck`
2. `v2_partnerstruck`
3. `v3_partnerstruck`

#### 5. SMARTDENT
1. `v1_smartdent`
2. `v2_smartdent`
3. `v3_smartdent`

#### 6. ERP
1. `v1_erp`
2. `v2_erp`
3. `v3_erp`

#### 7. KARDEX
1. `v1_kardex`
2. `v2_kardex`
3. `v3_kardex`

#### 8. GEMP (Gestión Empresarial Participativa)
1. `v1_gem`
2. `v2_gem`
3. `v3_gem`

#### 9. CLINIC MENTOR
1. `v1_mentor`
2. `v2_mentor`
3. `v3_mentor`

## 3. Rastreo de Clics (Etiquetas UTM)
Todos los enlaces incluyen los parámetros base: `utm_source=partnertech`, `utm_medium=correo`, `utm_term={{Email_Hash}}`.

### Valores de Campaña (`utm_campaign`) por Aplicativo:
- **CRM**: `campana_crm`
- **HCM**: `campana_hcm`
- **Nextflow**: `campana_nextflow`
- **Partners Truck**: `campana_partnerstruck`
- **SmartDent**: `campana_smartdent`
- **ERP**: `campana_erp`
- **Kardex**: `campana_kardex`
- **GEMP**: `campana_gem`
- **Clinic Mentor**: `campana_mentor`

### Valores de Contenido (`utm_content`) por Enlace:
Formato: `{plantilla}_{elemento}`. Fiel a las directrices, todo elemento cliqueable está etiquetado:

- **Botón principal (CTA):** `{plantilla}_boton_[accion]` (ej: `v1_crm_boton_agendar`)
- **Redes Sociales:** `{plantilla}_red_[red_social]` (ej: `v1_crm_red_linkedin`, `v1_crm_red_youtube`, `v1_crm_red_facebook`, `v1_crm_red_instagram`, `v1_crm_red_tiktok`, `v1_crm_red_twitter`)
- **Enlace a la web:** `{plantilla}_enlace_web` (ej: `v1_crm_enlace_web`)
- **Correo emisor:** `{plantilla}_enlace_correo` (ej: `v1_crm_enlace_correo`)
- **Enlace de remover:** `{plantilla}_enlace_remover` (ej: `v1_crm_enlace_remover`)
- **Vínculos de textos específicos:** `{plantilla}_texto_[referencia]` (ej: `v1_crm_texto_conoce_mas`)

---
Última actualización: 12 de marzo de 2026.

