# Lineamientos de Diseño: Email Marketing Partner Tech

Este documento establece los estándares obligatorios para la creación y modificación de todas las plantillas de correo electrónico de Partner Tech. Estos lineamientos garantizan consistencia visual, profesionalismo y cumplimiento legal.

## 1. Paleta de Colores Institucional

| Uso | Hex | Muestra | Descripción |
| :--- | :--- | :--- | :--- |
| **Principal / Títulos** | `#001556` | 🔵 | Azul marino para el encabezado y títulos destacados. |
| **Azul Eléctrico (Medio)** | `#1e53dd` | 🔷 | Azul corporativo para botones CTA, enlaces y detalles de jerarquía. |
| **Cyan (Acento)** | `#00e0ff` | 💎 | Cyan para el borde inferior de la cabecera y acentos destacados. |
| **Acción / Éxito** | `#1bde5d` | 🟢 | Verde para bordes de soluciones positivas. |
| **Dolor / Alerta** | `#ef4444` | 🔴 | Rojo para resaltar puntos de dolor o problemas. |
| **Fondo Wrapper** | `#f0f7ff` | 🔘 | Celeste muy ligero para el fondo exterior. |
| **Cuerpo (Contenedor)** | `#ffffff` | ⚪ | Fondo blanco para asegurar limpieza y legibilidad (Cuerpo y Redes Sociales). |
| **Texto General** | `#555555` | 🌚 | Gris para el cuerpo de texto general. |

## 2. Tipografía y Jerarquía (Poppins Only)

- **Fuente Obligatoria:** **Poppins** para todos los elementos del correo sin excepción.
- **Trato Literario:** Informal (**Tutear**). Usar "tú" y "contigo" para generar cercanía.
- **Jerarquía:**
  - **Títulos (H1/H2):** Peso `800` (Extra Bold).
  - **Subtítulos/Botones:** Peso `700` (Bold).
  - **Cuerpo:** Peso `400` (Regular) o `300` (Light) según el contexto.

## 3. Logotipos y Encabezado

- **Borde de Cabecera:** Borde inferior sólido de **Cyan** (`#00e0ff`) de **6px**.
- **Logo del Encabezado:** Altura máxima de **50px**. No debe dominar visualmente el diseño.
- **Tagline:** Incluir "Tu Socio Estratégico" alineado a la derecha, en mayúsculas, color `#a0aec0` y `letter-spacing: 2.2px`.

## 4. Estructura y Espaciado (Layout Ultra-Compacto)

- **Divisores:** **Queda prohibido el uso de líneas divisorias** (`hr`, bordes punteados o sólidos) entre secciones, firmas o pies de página.
- **Espaciado Mínimo:** Se prioriza un diseño denso y profesional.
  - Margen entre secciones de contenido: Máximo **16px**.
  - Padding de bloques de cierre (CTA): Máximo **16px**.
  - Espaciado entre el CTA y el texto de despedida: Máximo **16px**.
- **Layout Fluido:** El diseño debe sentirse continuo, sin interrupciones visuales que separen el contenido.

## 5. Botón de Llamada a la Acción (CTA)

Para garantizar que el emoji y el texto permanezcan siempre en una sola línea en todos los clientes de correo (incluyendo Gmail móvil y Outlook), se debe usar la siguiente estructura de **Tablas Anidadas**:

- **Estructura:** Tabla outer para centrado -> Celda interna con `bgcolor` y `border-radius` -> Enlace `<a>` -> Tabla inner con dos celdas (`<td>` para emoji y `<td>` para texto).
- **Estilo:**
  - `background-color: #1e53dd`.
  - `color: #ffffff !important`.
  - `border-radius: 8px`.
  - `padding: 12px 25px`.
  - `line-height: 1.2`.
  - `vertical-align: middle` en todas las celdas internas.
- **Texto Post-CTA (Mandatorio):** Incluir un **párrafo persuasivo** (mínimo 3-4 líneas) debajo del botón CTA.
  - Debe explicar los beneficios de la reunión o qué esperar de ella.
  - Alineación: Izquierda (para romper la simetría del botón centrado y mejorar la lectura).
  - Estilo: Letra ligeramente más pequeña (14px) y color `#555555`.

## 6. Firma y Redes Sociales

- **Firma:** Separación clara entre el emisor y la empresa. Sin línea divisoria central.
- **Redes Sociales:** Fondo blanco absoluto. Iconos circulares nativos distribuidos horizontalmente. **Sin bordes separadores**.

## 7. Footer y Cumplimiento Legal

Todos los correos deben incluir obligatoriamente en el pie de página:
1.  **Presentación clara del emisor.**
2.  **Mención de origen de datos:** "Esta información ha sido obtenida de la base de datos de la **Cámara de Comercio de Lima (CCL)**".
3.  **Link de baja de suscripción:** Claramente visible.
4.  **Estética:** Texto `#cbd5e0` sobre fondo blanco, sin líneas divisorias superiores.

## 8. Resaltado de Texto Estratégico (HTML Nativo)

- **Negritas (Strong Highlights):** Es obligatorio resaltar en **negrita** las frases clave dentro de los párrafos para guiar el "escaneo" del lector.
  - **REGLA TÉCNICA CRÍTICA:** Se debe utilizar exclusivamente la etiqueta HTML nativa `<strong>` para las negritas. **Queda terminantemente prohibido el uso de asteriscos (`**`)** en las plantillas HTML, ya que los clientes de correo no procesan Markdown y los mostrarían como texto plano.
- **Puntos de Dolor (Negativo):** Resaltar en **Rojo** (`#ef4444`).
- **Soluciones (Positivo):** Resaltar en **Azul Corporativo**.
- **Limitación:** El resaltado de color es para palabras clave o frases cortas, no para párrafos enteros.
