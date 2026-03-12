# Lineamientos de Diseño: Email Marketing Partner Tech

Este documento establece los estándares obligatorios para la creación y modificación de todas las plantillas de correo electrónico de Partner Tech. Estos lineamientos garantizan consistencia visual, profesionalismo y cumplimiento legal, inspirados en las mejores prácticas de la industria (HubSpot).

## 1. Paleta de Colores Institucional

| Uso | Hex | Muestra | Descripción |
| :--- | :--- | :--- | :--- |
| **Principal / Títulos** | `#001556` | 🔵 | Azul marino para el saludo (Hola...), títulos de secciones y encabezados. |
| **Azul Eléctrico (Medio)** | `#1e53dd` | 🔷 | Azul para jerarquía en detalles o enlaces secundarios. |
| **Acción (CTA)** | `#00e0ff` | 💎 | Cyan para el botón principal de agendamiento y acentos destacados. |
| **Secundario (Éxito)** | `#1bde5d` | 🟢 | Verde institucional para tarjetas de beneficios o detalles positivos. |
| **Fondo / Cuerpo** | `#ffffff` | ⚪ | Fondo blanco para asegurar limpieza y legibilidad móvil. |
| **Texto Secundario** | `#555555` | 🌚 | Gris para el cuerpo de texto general. |
| **Divisores Sutiles** | `#e2e8f0` | ⚪ | Gris muy claro para líneas de separación poco visibles. |
| **Footer Legal** | `#333c4e` | 🌑 | Fondo oscuro de baja visibilidad para el pie de página legal. |
| **Texto Footer** | `#718096` | 🔘 | Gris claro para el texto legal (baja relevancia visual). |

## 2. Tipografía Estándar
*   **Fuente Principal**: `Poppins`, sans-serif. Se debe forzar mediante `!important` en el CSS global.
*   **Encabezados**: Peso **Bold (700)**, color `#001556`.
*   **Cuerpo**: Peso **Regular (400)**, color `#555555`, interlineado `1.6`.

## 2. Principios de Diseño (Inspiración HubSpot)

Basado en las mejores prácticas de conversión, cada correo debe cumplir con:

1.  **Jerarquía Visual Clara**: Un solo mensaje principal por correo. El elemento más importante debe ser el CTA (Cyan).
2.  **Encabezado Premium (Dark Mode Style)**: 
    *   **Fondo**: Azul Marino (`#001556`) sólido.
    *   **Borde Inferior**: Verde Institucional (`#1bde5d`) de `6px`.
    *   **Logo**: Versión **Blanca** (Logo_ver1) centrada (máx `40px`).
    *   **Tagline**: Texto en blanco sutil (`#a0aec0`) para alto contraste.
3.  **Cuerpo Neutral**: 
    *   **NO usar Azul Marino en el texto**.
    *   **Color de Títulos y Saludos**: Usar Gris Carbón (`#333c4e`).
    *   **Texto de Cuerpo y Beneficios**: Gris suave (`#555555`) para máxima legibilidad.
4.  **Firma Corporativa**: Estructura de dos columnas, cargo en dos líneas y divisor vertical sutil.
    *   Los cargos deben evitar el uso de símbolos como "/" para separar jerarquías; preferir el salto de línea (`<br>`).
    *   La columna derecha de la firma debe contener el logo y los datos de contacto generales.

## 3. Detalles de Implementación Técnica

### A. Botón de Acción (CTA)
*   **Fondo**: `#00e0ff`.
*   **Sombra**: `rgba(0, 224, 255, 0.3)`.
*   **Forma**: Borde redondeado `50px`.
*   **Texto**: `color: #ffffff !important`, peso `700`.

### B. Prohibiciones
*   **NO usar fuentes alternativas**: Mantener la soberanía de `Poppins`.
*   **No usar asteriscos**: Convertirlos siempre a `<strong>`.
*   **Evitar redundancia**: No poner el logo más de 2 veces por correo.

---

## 5. Segmentación Dinámica

Placeholders obligatorios:
*   `{{Nombre_Contacto}}`: Personalización.
*   `{{Cargo_Remitente}}`: Jerarquía dinámica del remitente.
*   `{{Email_Hash}}`: Rastreo GA4 obligatorio en cada enlace.
