import os
import re
from urllib.parse import urlparse, urlencode, parse_qsl, urlunparse

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

REDIRECTOR_BASE_URL = "http://localhost:8000"  # ¡CAMBIAR POR EL DOMINIO FINAL DEL SERVIDOR EN PRODUCCIÓN!

def add_utms(url, campana, plantilla, elemento):
    url = url.replace("&amp;", "&")
    # if it's Jinja like {{CTA_Link}}, let's treat it carefully
    if url.startswith("{{CTA_Link}}"):
        base_url = "{{CTA_Link}}"
        query_str = url[len(base_url):]
        if query_str.startswith("?"):
            query_str = query_str[1:]
    else:
        parsed = urlparse(url)
        base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '', parsed.fragment))
        query_str = parsed.query

    params = dict(parse_qsl(query_str))
    
    # Overwrite tracking params (Mantenemos UTMs estándar como respaldo)
    params['utm_source'] = 'partnertech'
    params['utm_medium'] = 'correo'
    params['utm_campaign'] = campana
    params['utm_content'] = f'{plantilla}_{elemento}'
    params['utm_term'] = '{{Email_Hash}}'
    
    new_query = "&amp;".join([f"{k}={v}" for k, v in params.items()])
    if base_url == "{{CTA_Link}}":
        final_url_with_utms = f"{base_url}?{new_query}"
    else:
        parsed = urlparse(url)
        final_url_with_utms = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

    # Parámetros para el Redirector y Measurement Protocol
    redirector_params = {
        'url': final_url_with_utms,
        'cid': '{{Email_Hash}}',
        'campana': campana,
        'plantilla': plantilla,
        'contenido': f'{plantilla}_{elemento}'
    }
    
    from urllib.parse import quote
    # Codificar solo la variable URL, las variables Jinja no deben codificarse (%7B%7B...) porque fallan al procesar la plantilla
    redir_query_parts = []
    for k, v in redirector_params.items():
        if k == 'url':
            # Codificamos la url pero ignoramos los caracteres {{ }} de Jinja para que no se arruinen
            quoted_url = quote(v, safe='{}')
            redir_query_parts.append(f"{k}={quoted_url}")
        else:
            redir_query_parts.append(f"{k}={v}")
            
    redir_query = "&amp;".join(redir_query_parts)
    
    return f"{REDIRECTOR_BASE_URL}/clic?{redir_query}"

def process_file(filepath):
    folder = os.path.basename(os.path.dirname(filepath))
    filename = os.path.basename(filepath)
    
    campana, plantilla = get_app_info(folder, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update Pixel
    pixel_pattern = r'(https://www\.google-analytics\.com/g/collect\?v=2&amp;tid=G-FLPG7XG57W&amp;cid={{Email_Hash}}&amp;en=apertura_correo&amp;ep\.campana=)([^&]+)(&amp;ep\.plantilla=)([^"]+)(")'
    content = re.sub(pixel_pattern, rf'\g<1>{campana}\g<3>{plantilla}\g<5>', content)
    
    # Update all anchor tags
    a_tag_pattern = re.compile(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>')
    
    def replace_href(match):
        full_tag = match.group(0)
        href = match.group(1)
        
        # Determine element type
        elemento = 'enlace_general'
        if 'facebook.com' in href or 'fb.com' in href:
            elemento = 'red_facebook'
        elif 'instagram.com' in href:
            elemento = 'red_instagram'
        elif 'linkedin.com' in href:
            elemento = 'red_linkedin'
        elif 'tiktok.com' in href:
            elemento = 'red_tiktok'
        elif 'youtube.com' in href:
            elemento = 'red_youtube'
        elif 'whatsapp.com' in href:
            elemento = 'enlace_whatsapp'
        elif 'mailto' in href:
            if 'Remover' in href or 'remover' in href:
                elemento = 'enlace_remover'
            else:
                elemento = 'enlace_correo'
        elif '{{CTA_Link}}' in href:
            elemento = 'boton_principal'
        elif 'partnertech.pe' in href:
            elemento = 'enlace_web'
        
        new_href = add_utms(href, campana, plantilla, elemento)
        return full_tag.replace(href, new_href)
        
    content = a_tag_pattern.sub(replace_href, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {filepath}")

def main():
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
