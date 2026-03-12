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
1. `v1_centralizacion`
2. `v2_embudo`
3. `v3_ventas`
4. `v4_fidelizacion`
5. `v5_corto`
6. `v6_directo`
7. `v7_branding`

#### 2. HCM (Rankmi)
1. `v1_autogestion`
2. `v2_nomina`
3. `v3_desempeno`
4. `v4_bi`
5. `v5_onboarding`
6. `v6_clima`
7. `v7_branding`

#### 3. NEXTFLOW (BPM)
1. `v1_procesos`
2. `v2_documental`
3. `v3_aprobaciones`
4. `v4_digitalizacion`
5. `v5_corto`
6. `v6_cumplimiento`
7. `v7_branding`

#### 4. PARTNERS TRUCK
1. `v1_mantenimiento`
2. `v2_combustible`
3. `v3_neumaticos`
4. `v4_logistica`
5. `v5_corto`
6. `v6_disponibilidad`
7. `v7_branding`

#### 5. SMARTDENT
1. `v1_agenda`
2. `v2_pacientes`
3. `v3_clinico`
4. `v4_digitalizacion`
5. `v5_corto`
6. `v6_fidelizacion`
7. `v7_branding`

#### 6. ERP
1. `v1_rentabilidad`
2. `v2_control`
3. `v3_visibilidad`
4. `v4_digitalizacion`
5. `v5_corto`
6. `v6_gobierno`
7. `v7_branding`

#### 7. KARDEX
1. `v1_control`
2. `v2_trazabilidad`
3. `v3_valorizacion`
4. `v4_digitalizacion`
5. `v5_corto`
6. `v6_auditoria`
7. `v7_branding`

#### 8. GEMP (Gestión Empresarial Participativa)
1. `v1_centralizacion`
2. `v2_manufactura`
3. `v3_proyectos`
4. `v4_finanzas`
5. `v5_eficiencia`
6. `v6_seguridad`
7. `v7_branding`

#### 9. CLINIC MENTOR
1. `v1_rentabilidad`
2. `v2_agenda`
3. `v3_finanzas`
4. `v4_historia`
5. `v5_corto`
6. `v6_auditoria`
7. `v7_branding`

## 3. Rastreo de Clics (Etiquetas UTM)
Todos los enlaces incluyen los parámetros base: `utm_source=partnertech`, `utm_medium=correo`, `utm_term={{Email_Hash}}`.

### Valores de Campaña (`utm_campaign`) por Aplicativo:
- **CRM**: `campana_crm`
- **HCM**: `campana_hcm`
- **Nextflow**: `campana_nextflow`
- **Partners Truck**: `campana_truck`
- **SmartDent**: `campana_smartdent`
- **ERP**: `campana_erp`
- **Kardex**: `campana_kardex`
- **GEMP**: `campana_gem`
- **Clinic Mentor**: `campana_clinic`

### Valores de Contenido (`utm_content`) por Enlace:
Formato: `{plantilla}_{elemento}` (ej: `v1_centralizacion_boton_agendar`).

---
Última actualización: 12 de marzo de 2026.

