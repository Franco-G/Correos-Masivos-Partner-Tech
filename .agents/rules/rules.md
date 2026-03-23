---
trigger: always_on
---

# Reglas del Proyecto: Correos Masivos Partner Tech

## Automatización de Pruebas
- **Script de Envío:** `scripts/send_test_templates.py`
- **Regla:** Cada vez que el asistente (tú) realice una edición en cualquier archivo dentro de la carpeta `templates/`, DEBES ejecutar exclusivamente el script de envío de prueba para validar los cambios. Ya NO es necesario usar el navegador o subagentes de visualización para confirmar la recepción, bastará con el reporte de salida del script.
- **Correos Destino:** `guerrerofranco1429@gmail.com`, `negocios@partnertech.pe`, `acardozo@partnertech.pe`

## Estándares de Plantillas
- **Formato:** HTML basado en tablas para compatibilidad total con Outlook.
- **Variables:** Usar siempre `{{Variable}}` para que el sistema de envío pueda reemplazarlas.
- **Rastreo:** Incluir siempre el píxel de GA4 al final de la plantilla.
- **Assets:** Usar `cid:` para imágenes embebidas (Logo_ver1, Logo_Color, etc.).

## Mantenimiento de Diseño
- **Lineamientos Sugeridos:** `docs/DESIGN_GUIDELINES.md`
- **Regla:** Ante cualquier mejora de diseño, cambio estructural o adaptación de responsividad que se implemente y sea validada por el usuario, DEBES actualizar inmediatamente `docs/DESIGN_GUIDELINES.md` para reflejar el nuevo estándar. Esto evita la degradación visual en futuras iteraciones.
- **Enfoque Móvil:** Priorizar siempre diseños que apilen columnas y usen anchos fluidos.

## Registro de Transparencia de Skills
- **REGLA DE ORO:** Absolutamente TODAS las respuestas dirigidas al usuario que impliquen una mejora, cambio, análisis o reporte de estado, DEBEN listar la totalidad de las skills disponibles en el sistema, separándolas en **Globales** (sistema base) y **Locales** (propias del ecosistema Partner Tech).
- **RESALTADO:** Debes **resaltar en negrita** aquellas skills que han sido aplicadas o consultadas activamente para resolver la tarea actual.
- **MOTIVACIÓN:** Esto garantiza que el usuario siempre tenga visibilidad de las herramientas y marcos de trabajo (como Kaizen, Marketing Bible, etc.) que están moldeando el resultado.
