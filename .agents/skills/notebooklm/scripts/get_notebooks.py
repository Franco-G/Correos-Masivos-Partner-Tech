import json
import re
import sys
from pathlib import Path
from patchright.sync_api import sync_playwright

# Add skill dir to path
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

from scripts.browser_utils import BrowserFactory

def get_notebooks():
    print("Iniciando extracción de cuadernos...")
    playwright = None
    context = None
    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(
            playwright,
            headless=True
        )

        page = context.new_page()
        print("Navegando a NotebookLM...")
        # Aumentamos el timeout por si la página tarda en cargar
        page.goto("https://notebooklm.google.com", wait_until="networkidle", timeout=60000)

        try:
            print("Buscando cuadernos en la página...")
            page.wait_for_selector('.project-button-title', timeout=30000)
        except Exception as e:
            print("Error esperando los cuadernos. Tomando screenshot y HTML...")
            page.screenshot(path=str(skill_dir / "debug_notebooks.png"))
            html = page.evaluate('() => document.body.innerHTML')
            with open(skill_dir / "debug_notebooks.html", "w", encoding="utf-8") as f:
                f.write(html)
            
            print("Intentando extraer con un selector más general...")

        # Extraer nombres y URLs basados en los atributos id de los títulos
        notebooks_data = page.evaluate('''() => {
            const spans = Array.from(document.querySelectorAll('span.project-button-title'));
            return spans.map(span => {
                const name = span.textContent.trim();
                const idAttr = span.id || '';
                let notebookId = '';
                const match = idAttr.match(/^project-(.+)-title$/);
                if (match) {
                    notebookId = match[1];
                }
                return {
                    name: name,
                    url: notebookId ? `https://notebooklm.google.com/notebook/${notebookId}` : ''
                };
            }).filter(item => item.url !== '');
        }''')

        # Filtrar repetidos o URLs extrañas, y limpiar nombres
        unique_notebooks = {}
        for nb in notebooks_data:
            url = nb['url']
            name = nb['name']
            
            # Limpiar nombre
            name = name.split('\\n')[0].strip()

            if url not in unique_notebooks and name.startswith("App - "):
                unique_notebooks[url] = name

        print("\n--- Cuadernos encontrados ---")
        results = []
        for url, name in unique_notebooks.items():
            print(f"- {name}: {url}")
            results.append({"name": name, "url": url})
        
        # Guardar resultados para leerlos luego
        output_file = skill_dir / "notebooks_extracted.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print(f"\nGuardados {len(results)} cuadernos en {output_file}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if context: context.close()
        if playwright: playwright.stop()

if __name__ == "__main__":
    get_notebooks()
