# App Validator - Memory

## Proyecto: correos-masivos-partner-tech

### Arquitectura
- **Lenguaje:** Python 3.x con Tkinter (GUI)
- **Base de datos:** SQLite (`data/control_envios.db`)
- **Plantillas:** HTML en directorio `templates/`
- **Assets:** Imagenes en `assets/logos/` y `assets/benefits/`

### Patrones Identificados

#### Estructura del Proyecto
```
correos-masivos-partner-tech/
├── src/main.py          # Aplicacion monolitica (946 lineas)
├── templates/           # Plantillas HTML por aplicativo
├── data/                # Base de datos y logs
├── assets/              # Logos e iconos
└── docs/                # Documentacion de contexto
```

#### Patrones de Codigo
- Clase principal: `CorreoApp` (Tkinter)
- Tracking: Hash MD5 de email para GA4 Client ID
- Envio: SMTP_SSL con plantillas HTML
- Control de duplicados: SQLite con periodo configurable

### Problemas Recurrentes Detectados

#### Seguridad
1. **Credenciales hardcodeadas** - Requiere mover a `.env`
2. **SSL desactivado** - `context.verify_mode = ssl.CERT_NONE`
3. **Contrasenas en texto plano** - Perfiles de usuario expuestos

#### Threading
- Tkinter no es thread-safe - UI se modifica desde threads secundarios
- Necesita cola de mensajes + `root.after()`

#### Base de Datos
- Conexion nueva por operacion (ineficiente)
- Necesita patron singleton o pool de conexiones

### Dependencias (requirements.txt)
- pandas
- email-validator
- tkinterweb
- openpyxl (implicito para Excel)

### Configuracion SMTP
- Servidor: `mail.partnertech.pe`
- Puerto: 465 (SSL)
- Dominio de tracking: GA4 con parametros `utm_source`, `utm_campaign`

### Convenciones de Codigo
- Comentarios y UI en espanol
- Variables mezcladas ingles/espanol
- Type hints parciales (Pyre2)
- Archivo monolitico sin modularizar

### Archivos Importantes
- `.env` existe pero no se usa
- `data/registro_envios.csv` - Log de envios
- `data/registro_envios.log` - Log de aplicacion

### Proximas Acciones Sugeridas
1. Mover credenciales a `.env`
2. Implementar threading seguro
3. Refactorizar a modulos separados
4. Agregar validacion de archivos