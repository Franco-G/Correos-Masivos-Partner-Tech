import os
from PIL import Image

def colorize_png(source_path, target_path, hex_color):
    """
    Cambia el color de los píxeles no transparentes de un PNG a un color específico.
    hex_color: string en formato '#RRGGBB'
    """
    # Convertir hex a RGB
    hex_color = hex_color.lstrip('#')
    target_rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    img = Image.open(source_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        # item es (r, g, b, a)
        # Si no es totalmente transparente, le aplicamos el color manteniendo el alfa
        if item[3] > 0:
            # Podríamos ser más sofisticados con la escala de grises, 
            # pero para iconos negros de IcoMoon esto es ideal.
            new_data.append(target_rgb + (item[3],))
        else:
            new_data.append(item)

    img.putdata(new_data)
    
    # Asegurar directorio de destino
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    img.save(target_path)
    print(f"Generado: {target_path} con color {hex_color}")

# Configuración de iconos a generar
base_path = "assets/icons/icomoon"
output_path = "assets/icons/custom"

tasks = [
    ("084-calendar.png", "agenda_red.png", "#ef4444"),
    ("078-history.png", "history_green.png", "#1bde5d"),
    ("084-calendar.png", "agenda_navy.png", "#001556"),
    ("078-history.png", "history_navy.png", "#001556"),
    ("060-coin-dollar.png", "finance_navy.png", "#001556")
]

for source, dest, color in tasks:
    colorize_png(os.path.join(base_path, source), os.path.join(output_path, dest), color)
