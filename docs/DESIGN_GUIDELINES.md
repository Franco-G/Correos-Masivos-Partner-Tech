# Lineamientos de Diseño: Email Marketing Partner Tech

Este documento establece los estándares obligatorios para la creación y modificación de todas las plantillas de correo electrónico de Partner Tech. Estos lineamientos garantizan consistencia visual, profesionalismo y cumplimiento legal, inspirados en las mejores prácticas de la industria (HubSpot).

## 1. Paleta de Colores Institucional

| Uso | Hex | Muestra | Descripción |
| :--- | :--- | :--- | :--- |
| **Principal / Títulos** | `#001556` | 🔵 | Azul marino para el encabezado, bloques de cierre y títulos destacados. |
| **Azul Eléctrico (Medio)** | `#1e53dd` | 🔷 | Azul para jerarquía en detalles, enlaces y bordes de beneficios. |
| **Cyan (Acento)** | `#00e0ff` | 💎 | Cyan para acentos destacados y enlaces dentro de bloques oscuros. |
| **Acción / Éxito** | `#1bde5d` | 🟢 | Verde institucional para el botón principal de CTA y bordes de éxito. |
| **Fondo Wrapper** | `#eaeded` | 🔘 | Gris claro/azulado para el fondo exterior, resaltando el contenedor blanco. |
| **Cuerpo (Contenedor)** | `#ffffff` | ⚪ | Fondo blanco para asegurar limpieza y legibilidad móvil. |
| **Texto General** | `#555555` | 🌚 | Gris para el cuerpo de texto general. |
| **Texto Títulos** | `#333c4e` | 🌑 | Gris carbón para saludos y títulos de tarjetas (máximo contraste). |
| **Divisores Sutiles** | `#e2e8f0` | ⚪ | Gris muy claro para líneas de separación y bordes de tarjetas. |

## 2. Tipografía Estándar
*   **Fuente Principal**: `Poppins`, sans-serif. Se debe forzar mediante `!important` en el CSS global.
*   **Encabezados**: Peso **Bold (700)**, color `#333c4e` (cuerpo) o blanco (bloques oscuros).
*   **Cuerpo**: Peso **Regular (400)**, color `#555555`, interlineado `1.6`.

## 3. Iconografía Profesional (NUEVO ESTÁNDAR)
Queda prohibido el uso de emojis en los títulos de beneficios o botones. Se debe utilizar el sistema de iconos profesionales:
*   **Formato**: Iconos lineales (estilo Lucide), grosor de trazo `2px`.
*   **Implementación**: Adjuntos mediante `cid:Icon_Nombre` (ej. `cid:Icon_Agenda`).
*   **Dimensiones**: `18px` para títulos de beneficios, `16px` para botones.
*   **Alineación**: `vertical-align: middle; margin-right: 8px;`.
*   **Colores**: Los iconos deben coincidir exactamente con el color de acento de la tarjeta o ser blancos en botones.

## 4. Componentes Estructurales

### 4.1 Tarjetas de Beneficios (Benefit Cards)
*   **Estructura**: `background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; shadow: 0 4px 12px rgba(0, 0, 0, 0.04);`.
*   **Borde de Acento**: Borde izquierdo de `5px` con el color temático del beneficio.
*   **Título**: Título en negrita (`700`) con su icono correspondiente.

### 4.2 Bloque de Cierre y CTA (Navy Block)
*   **Fondo**: Azul Marino (`#001556`) sólido.
*   **Forma**: Bordes redondeados de `10px` (antes 20px) para un look más moderno y alineado a la UI del software.
*   **Botón CTA**: Fondo Verde (`#1bde5d`), radio de `10px`, texto blanco negrita, con icono de calendario blanco (`filter: brightness(0) invert(1)` si se usa el mismo CID).

### 4.3 Encabezado Premium
*   **Fondo**: Azul Marino (`#001556`) con borde inferior Verde (`#1bde5d`) de `6px`.
*   **Logo**: Versión **Blanca** (`cid:Logo_ver1`) de `50px` de altura.
*   **Tagline**: Texto `#a0aec0` de `12px`, peso `600`, en mayúsculas.

## 5. Firma y Footer

*   **Firma**: Fuera de bloques de color. Nombre en `#333c4e` (Bold), cargo en `#718096`. Logo a color (`cid:Logo_Color`) con altura máxima de `35px`.
*   **Footer**: Texto `#cbd5e0` de `12px`, centrado, sobre fondo blanco absoluto.

## 6. Placeholders y Rastreo
*   `{{Nombre_Contacto}}`: Personalización.
*   `{{Email_Hash}}`: Obligatorio en todos los enlaces y en el píxel de GA4.
*   **Píxel GA4**: Debe incluirse al final del `body` con los parámetros `en=apertura_correo`, `ep.campana` y `ep.plantilla` correctos.
