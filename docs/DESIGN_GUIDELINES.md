# Lineamientos de Diseño: Email Marketing Partner Tech

Este documento establece los estándares obligatorios para la creación y modificación de todas las plantillas de correo electrónico de Partner Tech. Estos lineamientos garantizan consistencia visual, profesionalismo y cumplimiento legal, inspirados en las mejores prácticas de la industria (HubSpot).

## 1. Paleta de Colores Institucional

| Uso | Hex | Muestra | Descripción |
| :--- | :--- | :--- | :--- |
| **Principal / Títulos** | `#001556` | 🔵 | Azul marino para el encabezado, bloques de cierre y títulos destacados. |
| **Azul Eléctrico (Medio)** | `#1e53dd` | 🔷 | Azul para jerarquía en detalles, enlaces y bordes de beneficios. |
| **Cyan (Acento)** | `#00e0ff` | 💎 | Cyan para acentos destacados y enlaces dentro de bloques oscuros. |
| **Acción / Éxito** | `#1bde5d` | 🟢 | Verde institucional para el botón principal de CTA y bordes de éxito. |
| **Fondo Wrapper** | `#f0f7ff` | 🔘 | Celeste muy ligero para el fondo exterior, resaltando el contenedor blanco. |
| **Cuerpo (Contenedor)** | `#ffffff` | ⚪ | Fondo blanco para asegurar limpieza y legibilidad móvil. |
| **Texto General** | `#555555` | 🌚 | Gris para el cuerpo de texto general. |
| **Texto Títulos** | `#333c4e` | 🌑 | Gris carbón para saludos y títulos de tarjetas (máximo contraste). |
| **Divisores Sutiles** | `#e2e8f0` | ⚪ | Gris muy claro para líneas de separación y bordes de tarjetas. |

## 2. Tipografía y Jerarquía (Poppins Only)

| Elemento | Tamaño | Peso (Weight) | Interlineado | Tracking | Color |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H1 (Hero)** | 36px | 800 (Extra Bold) | 1.1 | -1px | `#333c4e` |
| **H2 (Sección)** | 24px | 800 (Extra Bold) | 1.3 | 0 | `#001556` |
| **H3 (Tarjetas)**| 20px | 700 (Bold)       | 1.4 | 0 | `#1e293b` |
| **Saludo** | 17px | 700 (Bold)       | 1.4 | 0 | `#333946` |
| **Body (P)** | 16px | 400 (Regular)    | 1.62| 0 | `#64748b` |
| **Etiquetas** | 12px | 800 (Extra Bold) | Auto| 1.5px | *Variable* |
| **Slogan/Lema** | 11px | 600 (Semi Bold)  | Auto| 2.2px | `#a0aec0` |
| **Firma/Pie** | 13px | 400 (Regular)    | 1.5 | 0 | `#718096` |
| **Legal/Baja** | 11px | 400 (Regular)    | 1.6 | 0.3px | `#cbd5e0` |

> [!IMPORTANT]
> El uso de `Poppins` es obligatorio vía Google Fonts. Se debe incluir el peso `900` para títulos de máximo impacto si es necesario, pero el estándar es `800`.

## 3. Iconografía Profesional (Estándar IcoMoon PNG)
Queda prohibido el uso de archivos `.svg` y emojis en los beneficios o botones. El estándar oficial es la biblioteca **IcoMoon Free**:
*   **Formato**: PNG con transparencia (32px o 64px). **NO USAR SVG**.
*   **Ubicación**: `assets/icons/icomoon/`.
*   **Implementación**: Adjuntos mediante `cid:minimalist_[nombre]` (ej. `cid:minimalist_agenda`).
*   **Dimensiones en HTML**: Atributo `width="32"` o `width="24"` según el layout.
*   **Alineación**: `vertical-align: middle; margin-right: 8px;`.
*   **Iconos Sociales**: CIDs específicos `soc_fb`, `soc_ig`, `soc_li`.
*   **Procedimiento**: Los iconos se eligen de la base local y se mapean en el script de envío (`main.py` y `send_test_templates.py`).

## 4. Componentes Estructurales

### 4.1 Tarjetas de Beneficios (Benefit Cards)
*   **Estructura**: `background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; shadow: 0 4px 12px rgba(0, 0, 0, 0.04);`.
*   **Borde de Acento**: Borde izquierdo de `5px` con el color temático del beneficio.
*   **Título**: Título en negrita (`700`) con su icono correspondiente.

### 4.2 Bloque de Cierre y CTA (Navy Block)
*   **Fondo**: Azul Marino (`#001556`) sólido.
*   **Forma**: Bordes redondeados de `10px` (antes 20px) para un look más moderno y alineado a la UI del software.
*   **Botón CTA**: Fondo Verde (`#1bde5d`), radio de `10px`, texto blanco negrita, con icono de calendario blanco (`filter: brightness(0) invert(1)` si se usa el mismo CID).

### 4.3 Encabezado Premium Unificado (Final)
*   **Fondo**: Blanco absoluto (`#ffffff`) con borde inferior Cyan (`#00e0ff`) de `6px`.
*   **Logo**: Versión **Color** (`cid:Logo_Color`) de **60px** de altura, estandarizado para coincidir con el logo de la firma en formato de un solo color.
*   **Tagline**: "Tu Socio Estratégico" alineado a la **derecha** del logo. Texto `#a0aec0` de `11px`, peso `600`, en mayúsculas, con `letter-spacing: 2.2px`.

## 5. Firma y Footer

*   **Párrafo de Soporte**: Inmediatamente antes de la firma, se debe incluir un párrafo `espaciado-cuerpo` con el mensaje: "Estamos a su disposición para cualquier consulta. Puede agendar una llamada breve con nosotros o responder directamente a este correo."
*   **Firma**: Fuera de bloques de color. Nombre en `#333c4e` (Bold), cargo en `#718096`. Columnas sin línea divisora. Logo a color (`cid:Logo_Color`) con altura máxima de `35px`. Datos de contacto de la empresa sin incluir RUC.
*   **Redes Sociales**: Bloque centrado transversal justo antes del footer. La celda (`<td>`) contenedora **debe** tener un fondo blanco absoluto (`#ffffff`), ocupando el 100% del ancho del main-container. Uso obligatorio de tabla interior con `align="center"` y ancho fijo (`160px`). Iconos circulares transparentes a todo color de 24px (`logo_facebook_circular`, `logo_instagram_circular`, `logo_linkedin_circular`).
*   **Footer**: Texto `#cbd5e0` de `11px`, centrado, sobre fondo blanco absoluto. Incluye link de baja y mención a la CCL.

## 6. Placeholders y Rastreo
*   `{{Nombre_Contacto}}`: Personalización.
*   `{{Email_Hash}}`: Obligatorio en todos los enlaces y en el píxel de GA4.
*   **Píxel GA4**: Debe incluirse al final del `body` con los parámetros `en=apertura_correo`, `ep.campana` y `ep.plantilla` correctos.

## 7. Glosario de Clases CSS (Español)

| Clase Original (EN) | Clase Localizada (ES) | Propósito |
| :--- | :--- | :--- |
| `.wrapper` | `.envoltorio` | Contenedor externo de ancho completo del correo. |
| `.main-container` | `.contenedor-principal` | Caja central de 600px que contiene el diseño. |
| `.header` | `.cabecera` | Sección superior con logo y lema corporativo. |
| `.hero` | `.seccion-hero` | Bloque principal de impacto visual y mensaje clave. |
| `.title-hero` | `.titulo-hero` | Encabezado H1 de gran tamaño y peso visual. |
| `.section-padding` | `.espaciado-seccion` | Margen interno estándar para el cuerpo del texto. |
| `.impact-card` | `.tarjeta-impacto` | Tarjeta de comparación o impacto (Acento de color). |
| `.accent-red` | `.acento-rojo` | Variante con borde y fondo rojo ligero. |
| `.accent-green` | `.acento-verde` | Variante con borde y fondo verde ligero. |
| `.box-icon` | `.caja-icono` | Contenedor para iconos (ahora transparente). |
| `.navy-block` | `.bloque-navy` | Sección de llamado a la acción con fondo corporativo. |
| `.footer` | `.pie-pagina` | Sección de avisos legales y baja de suscripción. |
| `.stack-col` | `.columna-apilada` | Clase para que las columnas se apilen automáticamente en móvil. |
| `.signature-stack` | `.firma-apilada` | Específico para el apilado de la firma en móviles. |
