import os
import requests
import zipfile
import shutil

def main():
    url = "https://healthicons.org/icons.zip"
    zip_path = "temp_icons.zip"
    extract_path = "temp_icons_extracted"
    target_dir = "assets/icons_base"

    print(f"Descargando {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
    else:
        print(f"Error al descargar: {response.status_code}")
        return

    print("Extrayendo...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    print("Organizando iconos outline...")
    # Health Icons zip structure usually has folders like 'filled', 'outline', etc.
    # We want 'outline' and specifically PNGs if available, or we'll use SVGs.
    # Looking at the web, it seems they provide SVGs in the zip mainly.
    
    count = 0
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if 'outline' in root.lower() and file.endswith('.png'):
                # Copy to assets/icons_base
                src = os.path.join(root, file)
                # Keep category in name to avoid collisions
                category = os.path.basename(os.path.dirname(root))
                new_name = f"{category}_{file}"
                dst = os.path.join(target_dir, new_name)
                shutil.copy2(src, dst)
                count += 1
            elif 'outline' in root.lower() and file.endswith('.svg'):
                # Also keep SVGs just in case
                src = os.path.join(root, file)
                category = os.path.basename(os.path.dirname(root))
                # If there's an 'icons' parent, skip it
                if category == 'icons':
                    category = os.path.basename(os.path.dirname(os.path.dirname(root)))
                
                new_name = f"{category}_{file}"
                dst = os.path.join(target_dir, new_name)
                shutil.copy2(src, dst)
                count += 1

    print(f"Proceso completado. Se han copiado {count} iconos a {target_dir}")
    
    # Cleanup
    # os.remove(zip_path)
    # shutil.rmtree(extract_path)

if __name__ == "__main__":
    main()
