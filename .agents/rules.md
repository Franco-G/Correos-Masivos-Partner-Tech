# Reglas del Proyecto: Correos Masivos Partner Tech

## Automatización de Pruebas
- **Script de Envío:** `scripts/send_test_templates.py`
- **Regla:** Cada vez que el asistente (tú) realice una edición en cualquier archivo dentro de la carpeta `templates/`, DEBES ejecutar automáticamente el script de envío de prueba para validar que el diseño no se haya roto y que el usuario pueda verlo en su bandeja de entrada inmediatamente.
- **Correo Destino:** `guerrerofranco1429@gmail.com`

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
- **REGLA:** En cada respuesta que implique una mejora, cambio o análisis, debo listar **todas** las skills disponibles en el sistema.
- **REGLA:** Debo **resaltar en negrita** aquellas skills que están siendo activamente consultadas o aplicadas para resolver la petición actual del usuario.
