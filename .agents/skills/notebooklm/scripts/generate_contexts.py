import json
import os
import sys
import re
from pathlib import Path

# Add skill dir to path
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

from scripts.ask_question import ask_notebooklm

def get_safe_filename(name):
    """Convierte 'App - Nombre' en 'NOMBRE' sin espacios para el nombre del archivo"""
    # Remover 'App - '
    clean_name = name.replace("App - ", "")
    # Convertir a mayúsculas, reemplazar espacios por guiones bajos
    clean_name = clean_name.upper().replace(" ", "_")
    # Quitar caracteres especiales
    clean_name = re.sub(r'[^A-Z0-9_]', '', clean_name)
    return clean_name

def generate_contexts():
    # Leer resultados extraidos
    json_path = skill_dir / "notebooks_extracted.json"
    if not json_path.exists():
        print(f"No se encontró {json_path}. Ejecuta get_notebooks.py primero.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        notebooks = json.load(f)

    # Preparar el directorio de salida
    docs_dir = Path(r"C:\Users\USER\Documents\Repositorios\correos-masivos-partner-tech\docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    prompt = (
        "Actúa como un estratega de producto y marketing B2B. Basándote en todo el contenido y fuentes de este cuaderno, "
        "escribe un documento de Contexto Estratégico en formato Markdown estricto. "
        "Crea el contenido imitando exactamente la siguiente estructura y formato:\n\n"
        "# Contexto Estratégico: [Nombre del Sistema/App]\n\n"
        "Este documento detalla la base conceptual, técnica y de ventas utilizada para la creación de las 6 versiones de correo electrónico de la campaña. "
        "El objetivo es servir como referencia de 'Single Source of Truth' para entender por qué se eligieron ciertos ángulos y cómo cada versión ataca un dolor específico del sector.\n\n"
        "---\n\n"
        "## 1. Propuesta de Valor Central\n"
        "- **Problema Crítico:** (describe el problema principal que resuelve)\n"
        "- **Solución:** (describe cómo lo soluciona)\n\n"
        "---\n\n"
        "## 2. Definición de Ángulos por Versión\n"
        "Crea 6 ángulos distintos de ventas o marketing pensados para esta solución. Para cada uno detalla lo siguiente:\n\n"
        "### v1: El Ángulo [Nombre de la versión]\n"
        "- **Concepto:** ...\n"
        "- **Dolor:** ...\n"
        "- **Gancho:** ...\n\n"
        "### v2: ... (y así hasta v6)\n\n"
        "---\n\n"
        "## 3. Elementos Técnicos Comunes\n"
        "- **Modelo de Negocio:** ...\n"
        "- **Infraestructura:** ...\n"
        "- **Características Técnicas Clave:** ...\n\n"
        "---\n\n"
        "## 4. Segmentación Recomendada (ICP)\n"
        "La campaña está diseñada para impactar a:\n"
        "1. **[Perfil 1]:** Interesados en...\n"
        "2. **[Perfil 2]:** Interesados en...\n"
        "3. **[Perfil 3]:** Interesados en...\n\n"
        "NOTA: Genera SOLO el código Markdown resultante. No incluyas comentarios introductorios ni de despedida."
    )

    for nb in notebooks:
        name = nb["name"]
        url = nb["url"]
        
        safe_name = get_safe_filename(name)
        output_file = docs_dir / f"CONTEXTO_{safe_name}.md"

        if output_file.exists():
            print(f"Saltando {name}: El archivo ya existe en {output_file}")
            continue

        print(f"\nGenerando contexto para: {name}")
        
        # Consultar NotebookLM
        response = ask_notebooklm(question=prompt, notebook_url=url, headless=True)
        
        if response:
            # Limpiar la respuesta (por si NotebookLM añade Follow_up_reminder)
            # El script ask_question.py actual añade FOLLOW_UP_REMINDER al final. Lo limpiamos.
            if "EXTREMELY IMPORTANT:" in response:
                response = response.split("EXTREMELY IMPORTANT:")[0].strip()
            
            # Limpiar tags ```markdown si existen
            response = re.sub(r'^```markdown\n?', '', response, flags=re.MULTILINE)
            response = re.sub(r'\n?```$', '', response, flags=re.MULTILINE)
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response)
            
            print(f"✅ Contexto guardado en {output_file}")
        else:
            print(f"❌ Error al generar contexto para {name}")

if __name__ == "__main__":
    generate_contexts()
