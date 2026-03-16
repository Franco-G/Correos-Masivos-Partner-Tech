# Partner Tech | Gestor de Envío Masivo 🚀

Una aplicación de escritorio profesional desarrollada en Python para la gestión y automatización de campañas de correo electrónico masivo, optimizada para **Partner Tech**.

<img src="https://img.shields.io/badge/Python-3.8-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/UI-Tkinter-0021a4?style=for-the-badge&logo=window-restore&logoColor=white" alt="Tkinter">
<img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/Analytics-GA4-orange?style=for-the-badge&logo=google-analytics&logoColor=white" alt="GA4">
<img src="https://img.shields.io/badge/Design-Poppins-1bde5d?style=for-the-badge" alt="Design">

## 🌟 Características Avanzadas

### 🛡️ Seguridad y Entregabilidad (SQLite)
El sistema integra una base de datos **SQLite local** (`data/control_envios.db`) que actúa como un cerebro histórico:
- **Enfriamiento de Contactos:** Evita saturar a los clientes forzando un periodo de espera configurable (default: 15 días).
- **Control de Duplicados:** Salta automáticamente a destinatarios que hayan recibido el mismo u otro correo en el ciclo actual.
- **Estadísticas en Tiempo Real:** Visualización de envíos totales y contactos únicos alcanzados.

### 🔄 Rotación Cíclica de Plantillas
Permite configurar **hasta 3 plantillas diferentes** por envío masivo, las cuales se distribuyen de forma equitativa y aleatoria para mitigar los filtros de spam.

### 📊 Trazabilidad GA4 "Privacy-First"
- **Anonimización PII:** Genera un **Hash MD5** único (`Email_Hash`) para el `client_id`.
- **Eventos Automáticos:** Registra `open_email` mediante un píxel de rastreo invisible de 1x1.

---

## 🔍 Fundamentación y Estrategia por Aplicativo

Cada campaña es el resultado de una investigación profunda detallada en `/docs/`. A continuación, el resumen estratégico de las soluciones principales:

### 🏗️ 1. Infrasys (Obras e Ingeniería)
*   **Rubro:** Construcción, Minería, Ingeniería Vial y Acabados (46 sub-rubros identificados).
*   **Contexto Estratégico:** Migración del modelo SaaS (alquiler) a **Licencia Perpetua**. Ataca el dolor de la "Fatiga de Rentas" y la necesidad de soberanía de datos sobre activos de obra críticos.
*   **Benchmarking:** Supera a competidores como *BrickControl* eliminando el pago por usuario y a *S10* mediante una interfaz moderna e interoperable.
*   **Ángulos Clave:** Soberanía Tecnológica, Inversión vs. Gasto, Cero Rentas.

### 🏥 2. Clinic Mentor (Salud y Formación)
*   **Rubro:** Centros Médicos Híbridos, Instituciones Académicas de Salud.
*   **Contexto Estratégico:** Centralización administrativa para eliminar el desorden de pacientes y deudas. Fuerte enfoque en el blindaje financiero.
*   **Benchmarking (Plan Mejora):** Integración única de "Historia Clínica + Gestión Académica + Conciliación Bancaria Automática".
*   **Ángulos Clave:** Admisión Inteligente, Sincronización Bancaria (TXT), Dashboard de Productividad.

### 🚛 3. Partners Truck (Logística y Flotas)
*   **Rubro:** Transporte de carga, Operadores Logísticos, Gestión de activos móviles.
*   **Contexto Estratégico:** Transformar la incertidumbre del viaje en rentabilidad predictiva. Enfoque en el control granular por kilómetro.
*   **Benchmarking:** Integración nativa con RENIEC/SUNAT para validación de conductores (Cero Errores) y Mantenimiento Predictivo con IA.
*   **Ángulos Clave:** Visibilidad 360° (GPS), Margen Real por Viaje, Mantenimiento 4.0.

### 🤝 4. CRM (Ventas y Relaciones)
*   **Rubro:** Equipos Comerciales, B2B, Servicios Profesionales.
*   **Contexto Estratégico:** Asegurar la **Memoria Institucional**. Evitar que la información sea propiedad de vendedores individuales.
*   **Benchmarking:** Enfoque de hiper-productividad (cotizaciones en < 60s) y omnicanalidad (Email/WhatsApp unificado).
*   **Ángulos Clave:** Adiós al Excel, Velocidad de Cierre, Memoria Digital.

### 📄 5. Nexflow (Gestión Documental y BPM)
*   **Rubro:** Comercio Exterior, Áreas Legales, Logística Documental.
*   **Contexto Estratégico:** Orquestación de procesos sin papel. Entrega del **código fuente** para soberanía tecnológica absoluta.
*   **Benchmarking:** Automatización mediante flujos BPMN 2.0 y firmas digitales PKI con validez legal.
*   **Ángulos Clave:** Ni un Papel Perdido, Soberanía Tecnológica, Agilidad Sin Código.

### 📦 6. Kardex (Inventarios Inteligentes)
*   **Rubro:** Almacenes, Retail, Farmacéuticas (Control de Lotes).
*   **Contexto Estratégico:** Trazabilidad absoluta y eliminación de discrepancias entre stock físico y contable.
*   **Benchmarking:** Lógica FEFO (vencimiento) automatizada e inventario predictivo mediante IA para optimizar capital de trabajo.
*   **Ángulos Clave:** Integridad Financiera, Trazabilidad Crítica, Abastecimiento Inteligente.

---

## 🎨 Paleta de Colores Institucional

| Uso | Hex | Muestra |
| :--- | :--- | :---: |
| **Principal / Títulos** | `#001556` | 🟦 |
| **Azul Eléctrico** | `#1e53dd` | 🟦 |
| **Cyan (Acento)** | `#00e0ff` | 💠 |
| **Éxito / Botones** | `#1bde5d` | 🟩 |

## 🧪 Pruebas de Envío (Panel de Calidad)
- **Envío Múltiple:** Prueba todas o una selección de plantillas enviándolas a tu correo personal.
- **Simulación Real:** Respeta los intervalos (10-15s) para asegurar que el servidor SMTP procese los CIDs.

## 📦 Estructura de Activos (CIDs)
Utiliza **Content-ID (CID)** para asegurar la visualización inmediata:
- **Visualización Instantánea:** Las imágenes viajan dentro del correo, evitando bloqueos.
- **Independencia de Hosting:** Codificación directa desde `/assets`.

## 📂 Campañas Disponibles
- **🏗️ Infraestructura/Logística:** `infrasys`, `kardex`, `partners_truck`, `nextflow`.
- **🏥 Salud:** `clinic_mentor`, `smart_dent`.
- **💼 Gestión:** `erp`, `crm`, `hcm`, `gemp`.

## 🛠️ Instalación y Uso Rápido
1. **Requisitos:** Python 3.8+ y `pip install -r requirements.txt`.
2. **Setup:** Configura tu perfil de remitente.
3. **Draft:** Carga el archivo de destinatarios.
4. **Deploy:** Define el periodo de espera e **🚀 INICIAR ENVÍO**.

## 📚 Documentación Técnica
- [🎨 Lineamientos de Diseño](docs/DESIGN_GUIDELINES.md)
- [📊 Estrategia de Rastreo GA4](docs/GUIA_RASTREO_GA4.md)
- [🔍 Análisis de Benchmark & Rubros](docs/)

## 📈 Anexo: Métricas y Esfuerzo de Desarrollo

Este proyecto representa una implementación de alta complejidad que integra investigación de mercados, ingeniería de software y diseño avanzado. El nivel de detalle y personalización alcanzado es el resultado de un proceso intensivo y riguroso:

### 📊 Cuadro de Esfuerzo Acumulado
| Métrica | Cantidad / Valor | Detalle |
| :--- | :--- | :--- |
| **Interacciones (Prompts)** | **+250 Peticiones** | Ciclos de refinamiento detallado, auditoría y corrección de lógica. |
| **Tiempo de Ejecución** | **+60 Horas** | Investigación, arquitectura de código, diseño MJML y pruebas de envío. |
| **Documentación Estratégica** | **42 Archivos `.md`** | 11 de Rubros, 10 de Benchmarks y 21 de Contexto de Producto. |
| **Ecosistema de Plantillas** | **+70 Versiones HTML** | 7 variantes premium (v1-v7) por cada una de las 10 aplicaciones. |
| **Base de Conocimientos** | **+160k Caracteres** | Volumen total de investigación y fundamento técnico procesado. |

### 🛠️ Desafíos de Alta Complejidad Superados
1.  **Ingeniería de Entregabilidad**: Implementación de lógica **CID (Content-ID)** y rotación de plantillas para evadir filtros de spam y asegurar la visualización de imágenes sin acción del usuario.
2.  **Arquitectura de Datos (SQLite)**: Desarrollo de un sistema de "memoria histórica" para el control de duplicados y periodos de enfriamiento, garantizando la reputación del dominio remitente.
3.  **Trazabilidad Avanzada**: Integración con GA4 mediante Measurement Protocol, usando **hashing MD5** para cumplir con normativas de privacidad (GDPR/AP) sin perder métricas de conversión.
4.  **Consistencia de Marca**: Creación de una guía de estilo (`DESIGN_GUIDELINES.md`) que unifica tipografía (Poppins), iconografía (IcoMoon) y componentes UI en todos los aplicativos.

> [!NOTE]
> Este no es un script de envío simple; es una infraestructura escalable de **Email Marketing B2B** construida con precisión quirúrgica para maximizar la tasa de conversión en el sector corporativo.

---
**Desarrollado por Franco Guerrero | Partner Tech | 2026**
