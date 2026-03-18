import os
import re
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode

def get_app_info(folder, filename):
    mapping = {
        'crm': 'crm',
        'erp': 'erp',
        'gemp': 'gem',
        'hcm': 'hcm',
        'infrasys': 'infrasys',
        'kardex': 'kardex',
        'nextflow': 'nextflow',
        'partners_truck': 'partnerstruck',
        'smart_dent': 'smartdent',
        'clinic_mentor': 'mentor'
    }
    
    if folder == 'base':
        if 'diseno_a' in filename:
            return '{{Campana}}', 'base_a'
        elif 'diseno_b' in filename:
            return '{{Campana}}', 'base_b'
        elif 'diseno_c' in filename:
            return '{{Campana}}', 'base_c'
        else:
            return '{{Campana}}', 'base_desconocido'
            
    app_key = mapping.get(folder, folder)
    campana = f'campana_{app_key}'
    
    match = re.search(r'_(v\d+)_', filename)
    version = match.group(1) if match else 'v1'
    plantilla = f'{version}_{app_key}'
    
    return campana, plantilla

def clean_and_add_utms(url, campana, plantilla, elemento):
    # 1. Limpiar envolturas de localhost si existen
    from urllib.parse import unquote
    while "localhost:8000/clic?url=" in url:
        match = re.search(r'url=([^&]+)', url)
        if match:
            url = unquote(match.group(1))
        else:
            break
            
    # 2. Separar base y query
    if url.startswith("{{CTA_Link}}"):
        base_url = "{{CTA_Link}}"
        query_str = ""
    else:
        # Normalizar separadores antes de parsear
        url = url.replace("&amp;", "&").replace("&amp%3B", "&").replace("%3B", "&")
        parsed = urlparse(url)
        base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '', parsed.fragment))
        query_str = parsed.query

    # 3. Filtrar parámetros (eliminar UTMs previos y otros rastreos sucios)
    prev_params = parse_qsl(query_str)
    keep_params = []
    for k, v in prev_params:
        if k.startswith('utm_') or k in ['cid', 'campana', 'plantilla', 'contenido']:
            continue
        keep_params.append((k, v))
        
    # 4. Añadir UTMs frescos
    keep_params.append(('utm_source', 'partnertech'))
    keep_params.append(('utm_medium', 'correo'))
    keep_params.append(('utm_campaign', campana))
    keep_params.append(('utm_content', f'{plantilla}_{elemento}'))
    keep_params.append(('utm_term', '{{Email_Hash}}'))
    
    # 5. Reconstruir
    new_query = urlencode(keep_params, safe='{}') # Mantener llaves Jinja sin codificar si es posible
    
    # URL final (usamos &amp; para HTML)
    final_query = new_query.replace("&", "&amp;")
    
    if base_url == "{{CTA_Link}}":
        return f"{base_url}?{final_query}"
    
    return f"{base_url}?{final_query}"

def process_file(filepath):
    folder = os.path.basename(os.path.dirname(filepath))
    filename = os.path.basename(filepath)
    
    campana, plantilla = get_app_info(folder, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Limpieza inicial de cualquier residuo visual
    content = content.replace("http://localhost:8000/clic?url=", "")
    
    # Actualizar Píxel de Apertura (Simplificado y limpio)
    pixel_pattern = r'(https://www\.google-analytics\.com/g/collect\?v=2&tid=G-FLPG7XG57W&cid={{Email_Hash}}&en=apertura_correo&ep\.campana=)([^&]+)(&ep\.plantilla=)([^"]+)(")'
    content = re.sub(pixel_pattern, rf'\g<1>{campana}\g<3>{plantilla}\g<5>', content)
    
    # Actualizar enlaces <a>
    # Buscamos el href y capturamos todo el tag para contexto (como el estilo del botón WA)
    a_tag_pattern = re.compile(r'(<a\s+[^>]*href=["\'])([^"\']+)(["\'][^>]*>)')
    
    def replace_href(match):
        prefix = match.group(1)
        href = match.group(2)
        suffix = match.group(3)
        full_tag = match.group(0)
        
        # Auditoría de Redes Reales (Solo estas 3 existen según auditoría)
        elemento = 'enlace_general'
        if 'facebook.com' in href:
            elemento = 'red_facebook'
        elif 'instagram.com' in href:
            elemento = 'red_instagram'
        elif 'linkedin.com' in href:
            elemento = 'red_linkedin'
        elif 'whatsapp.com' in href or 'api.whatsapp' in href:
            if 'background-color: #1bde5d' in full_tag or 'background-color:#1bde5d' in full_tag:
                elemento = 'boton_whatsapp'
            else:
                elemento = 'enlace_whatsapp'
        elif 'mailto' in href:
            if 'Remover' in href or 'remover' in href or 'subject=Remover' in href:
                elemento = 'enlace_remover'
            else:
                elemento = 'enlace_correo'
        elif '{{CTA_Link}}' in href:
            elemento = 'boton_principal'
        elif 'partnertech.pe' in href:
            elemento = 'enlace_web'
        
        new_href = clean_and_add_utms(href, campana, plantilla, elemento)
        return f"{prefix}{new_href}{suffix}"
        
    content = a_tag_pattern.sub(replace_href, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
