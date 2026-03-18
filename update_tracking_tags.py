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

def clean_and_add_utms(url, app_campaign, plantilla, elemento):
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
        url = url.replace("&amp;", "&").replace("&amp%3B", "&").replace("%3B", "&")
        parsed = urlparse(url)
        base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '', parsed.fragment))
        query_str = parsed.query

    # 3. Filtrar parámetros previos
    prev_params = parse_qsl(query_str)
    keep_params = []
    for k, v in prev_params:
        if k.startswith('utm_') or k in ['cid', 'campana', 'plantilla', 'contenido']:
            continue
        keep_params.append((k, v))
        
    # 4. Determinar Campaña y Content (Estrategia Universal)
    final_campaign = app_campaign
    
    if elemento in ['red_facebook', 'red_instagram', 'red_linkedin']:
        final_campaign = 'redes_sociales'
    elif elemento == 'enlace_web':
        final_campaign = 'sitio_web'
    elif elemento == 'enlace_remover':
        final_campaign = 'legal'
    # WhatsApp y boton_cta mantienen final_campaign = app_campaign (fijado arriba)
        
    # Si es universal no le ponemos el prefijo de plantilla, pero si es del aplicativo sí
    final_content = elemento
    if final_campaign == app_campaign:
        final_content = f"{plantilla}_{elemento}"
        
    keep_params.append(('utm_source', 'partnertech'))
    keep_params.append(('utm_medium', 'correo'))
    keep_params.append(('utm_campaign', final_campaign))
    keep_params.append(('utm_content', final_content))
    keep_params.append(('utm_term', '{{Email_Hash}}'))
    
    # 5. Reconstruir
    new_query = urlencode(keep_params, safe='{}')
    final_query = new_query.replace("&", "&amp;")
    
    if base_url == "{{CTA_Link}}":
        return f"{base_url}?{final_query}"
    
    return f"{base_url}?{final_query}"

def process_file(filepath):
    folder = os.path.basename(os.path.dirname(filepath))
    filename = os.path.basename(filepath)
    
    app_campaign, plantilla = get_app_info(folder, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace("http://localhost:8000/clic?url=", "")
    
    # Píxel de Apertura: Sigue usando la del aplicativo para no perder el dato de qué producto están abriendo
    pixel_pattern = r'(https://www\.google-analytics\.com/g/collect\?v=2&tid=G-FLPG7XG57W&cid={{Email_Hash}}&en=apertura_correo&ep\.campana=)([^&]+)(&ep\.plantilla=)([^"]+)(")'
    content = re.sub(pixel_pattern, rf'\g<1>{app_campaign}\g<3>{plantilla}\g<5>', content)
    
    # Actualizar enlaces <a>
    a_tag_pattern = re.compile(r'(<a\s+[^>]*href=["\'])([^"\']+)(["\'][^>]*>)')
    
    def replace_href(match):
        prefix = match.group(1)
        href = match.group(2)
        suffix = match.group(3)
        full_tag = match.group(0)
        
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
            elemento = 'boton_cta' # Anteriormente boton_principal
        elif 'partnertech.pe' in href:
            elemento = 'enlace_web'
        
        new_href = clean_and_add_utms(href, app_campaign, plantilla, elemento)
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
