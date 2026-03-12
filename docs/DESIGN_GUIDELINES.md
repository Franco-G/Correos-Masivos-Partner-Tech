# Lineamientos de Diseño: Email Marketing Partner Tech

Este documento establece los estándares obligatorios para la creación y modificación de todas las plantillas de correo electrónico de Partner Tech. Estos lineamientos garantizan consistencia visual, profesionalismo y cumplimiento legal, inspirados en las mejores prácticas de la industria (HubSpot).

## 1. Paleta de Colores Institucional

| Uso | Hex | Muestra | Descripción |
| :--- | :--- | :--- | :--- |
| **Principal / Títulos** | `#001556` | 🔵 | Azul marino para títulos, párrafos destacados y negritas. |
| **Azul Eléctrico (Medio)** | `#1e53dd` | 🔷 | Azul para jerarquía en tarjetas o detalles (Usar con moderación). |
| **Acción (CTA)** | `#00e0ff` | 💎 | Cyan para el botón principal de agendamiento y acentos destacados. |
| **Secundario (Éxito)** | `#1bde5d` | 🟢 | Verde institucional para tarjetas de beneficios o detalles positivos. |
| **Fondo / Cuerpo** | `#ffffff` | ⚪ | Fondo blanco para asegurar limpieza y legibilidad móvil. |
| **Texto Secundario** | `#555555` | 🌚 | Gris para el cuerpo de texto general. |
| **Footer Legal** | `#333c4e` | 🌑 | Fondo oscuro de baja visibilidad para el pie de página legal. |
| **Texto Footer** | `#718096` | 🔘 | Gris claro para el texto legal (baja relevancia visual). |

## 2. Principios de Diseño (Inspiración HubSpot)

Basado en las mejores prácticas de conversión, cada correo debe cumplir con:

1.  **Jerarquía Visual Clara**: Un solo mensaje principal por correo. El elemento más importante debe ser el CTA (verde).
2.  **Personalización Profunda**: No solo el nombre, sino adaptar el tono según el aplicativo (salud en Clinic Mentor, logística en Kardex).
3.  **Finitud y Brevedad**: Párrafos cortos de máximo 3-4 líneas para facilitar el escaneo visual.
4.  **Diseño Mobile-First**: Ancho máximo de 600px, botones grandes y fáciles de tocar.
5. ### A. Encabezado Premium (Diseño de Franja)
*   **Fondo**: Blanco puro (`#ffffff`).
*   **Logo**: Centrado, altura máx `40px`.
*   **Franja de Cierre**: Una franja sólida de color `#001556` (institucional) de `8px` de altura en la base del encabezado.
*   **Tagline**: Texto en `#718096`, fuente Orbitron, `9px`, espaciado `2px`.
2.  **Cuerpo del Mensaje**:
    *   Saludo: `Hola {{Nombre_Contacto}},`
    *   Problema: Presentación del punto de dolor.
    *   Solución: Breve descripción del beneficio del software.
3.  **Bloque de Beneficios**: 1 a 3 cajas con bordes variados (`#1e53dd`, `#00e0ff`, `#1bde5d`).
4.  **Botón de Acción (Cyan)**: Centrado y destacado.
5.  **Firma con Confianza**: Datos del remitente, logo y enlace web con UTMs.
6.  **Pie de Página Legal (Baja Visibilidad)**: Información de cumplimiento CCL y link de baja.

---

## 4. Detalles de Implementación Técnica

### A. Botón de Acompañamiento (CTA)
*   **Fondo**: `#00e0ff`.
*   **Sombra**: `rgba(0, 224, 255, 0.3)`.
*   **Forma**: Borde redondeado `50px`.
*   **Importante**: Siempre usar `color: #ffffff !important` para el texto.

### B. Elementos de Acento (#1e53dd)
*   **Divisores**: Todas las líneas divisoras (punteadas, sólidas o barras verticales) deben ser de color **Azul Eléctrico (#1e53dd)** para mantener la consistencia visual.
*   **Otros usos**: Puntos de lista (viñetas) y detalles decorativos sutiles.
### C. Prohibiciones
*   **NO usar asteriscos**: Convertirlos siempre a `<strong>`.
*   **Evitar redundancia**: No poner el logo más de 2 veces por correo.
*   **No usar fondos oscuros en el cuerpo**: Mantener el contraste alto (texto oscuro sobre fondo claro).

---

## 5. Segmentación Dinámica

Recordar el uso correcto de los placeholders:
*   `{{Nombre_Contacto}}`: Para tono cercano.
*   `{{Nombre_Remitente}}`: Para autoría del mensaje.
*   `{{Email_Hash}}`: Obligatorio en todos los enlaces para rastreo GA4.
