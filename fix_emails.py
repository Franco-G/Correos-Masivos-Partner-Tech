import os

d = 'c:/Users/USER/Documents/Repositorios/correos-masivos-partner-tech/templates'
c = 0
for r, _, fs in os.walk(d):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(r, f)
            with open(p, 'r', encoding='utf-8') as file:
                txt = file.read()
            
            # Reemplazar negocios@partnertech.pe suelto (que termina en <br> o similar)
            # Primero nos aseguramos de que no esté ya dentro de un href
            if 'negocios@partnertech.pe<br>' in txt and '<a href="mailto:negocios@partnertech.pe"' not in txt:
                txt = txt.replace('negocios@partnertech.pe<br>', 
                                  '<a href="mailto:negocios@partnertech.pe" style="color: #64748b; text-decoration: none;">negocios@partnertech.pe</a><br>')
                with open(p, 'w', encoding='utf-8') as fw:
                    fw.write(txt)
                c += 1

print(f"Plantillas actualizadas con correo de empresa clicleable: {c}")
