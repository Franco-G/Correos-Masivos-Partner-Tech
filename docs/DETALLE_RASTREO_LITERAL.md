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

### Ejemplos en Código (Anatomía del Enlace)

Todos los enlaces en los correos HTML siguen esta estructura de etiquetas UTM estándar:

```html
<a href="https://[URL_DESTINO]?utm_source=partnertech&utm_medium=correo&utm_campaign=campana_[APP]&utm_content=[PLANTILLA]_[ELEMENTO]&utm_term={{Email_Hash}}">
```

**Ejemplo - Botón Principal (CRM v1):**
```html
<a href="{{CTA_Link}}?utm_source=partnertech&utm_medium=correo&utm_campaign=campana_crm&utm_content=v1_crm_boton_principal&utm_term={{Email_Hash}}">
```

**Ejemplo - Red Social LinkedIn (HCM v2):**
```html
<a href="https://linkedin.com/company/partner-tech?utm_source=partnertech&utm_medium=correo&utm_campaign=campana_hcm&utm_content=v2_hcm_red_linkedin&utm_term={{Email_Hash}}">
```

**Ejemplo - Enlace de Cancelar Suscripción (Kardex v3):**
```html
<a href="mailto:remover@partner-tech.com?utm_source=partnertech&utm_medium=correo&utm_campaign=campana_kardex&utm_content=v3_kardex_enlace_remover&utm_term={{Email_Hash}}">
```

---
Última actualización: 18 de marzo de 2026. (Estandarización UTM GA4)

