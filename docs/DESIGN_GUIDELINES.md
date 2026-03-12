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
2.  **Encabezado Premium (High Contrast)**: 
    *   **Fondo**: Azul Marino (`#001556`) sólido con borde inferior Verde (`#1bde5d`) de `6px`.
    *   **Logo**: Versión **Blanca** (Logo_ver1) de `50px` de altura.
    *   **Tagline**: Texto en blanco sutil (`#a0aec0`) de `12px` para máxima legibilidad.
3.  **Cuerpo y Texto**: 
    *   **NO usar Azul Marino en el texto del cuerpo**.
    *   **Títulos/Saludos**: Gris Carbón (`#333c4e`).
    *   **Párrafos**: Gris suave (`#555555`).
4.  **Sección de Cierre (CTA Navy Block)**:
    *   **Fondo**: Azul Marino (`#001556`) sólido.
    *   **Forma**: Bordes redondeados de `20px` y padding generoso.
    *   **Botón**: Azul Cyan (`#00e0ff`) o Verde (`#1bde5d`) con texto blanco negrita. En esta iteración se prefiere **Verde** para el botón sobre fondo marino.
    *   **Contraste**: Todos los textos dentro de este bloque deben ser claros (#a0aec0 o blanco).
5.  **Firma Corporativa (Fuera del Bloque)**: 
    *   **Ubicación**: Siempre fuera de bloques de color, directamente sobre el fondo blanco.
    *   **Colores**: Usar Gris Carbón (`#333c4e`) para el nombre y Gris Suave (`#718096`) para cargos y contacto.
    *   **Logo**: Usar la versión a **color** (`cid:Logo_Color`).
6.  **Pie de Página (Footer Clean)**:
    *   **Fondo**: Blanco (`#ffffff`) absoluto.
    *   **Texto**: Gris muy tenue (`#cbd5e0`) de `12px`.
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
 Riverside:0.0.0.0,
 Riverside:0.0.0.0,
 Riverside:0.0.1,
*   **NO usar fuentes alternativas**: Mantener la soberanía de `Poppins`.
*   **No usar asteriscos**: Convertirlos siempre a `<strong>`.
*   **Evitar redundancia**: No poner el logo más de 2 veces por correo.

---

## 5. Segmentación Dinámica

Placeholders obligatorios:
*   `{{Nombre_Contacto}}`: Personalización.
*   `{{Cargo_Remitente}}`: Jerarquía dinámica del remitente.
*   `{{Email_Hash}}`: Rastreo GA4 obligatorio en cada enlace.
