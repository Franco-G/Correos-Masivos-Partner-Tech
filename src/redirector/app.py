import os
import json
import httpx
from urllib.parse import unquote
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GA4 Click Redirector")

GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID", "G-FLPG7XG57W")
GA4_API_SECRET = os.getenv("GA4_API_SECRET", "YOUR_API_SECRET_HERE") 

async def send_ga4_event(cid: str, campana: str, plantilla: str, contenido: str, destino: str, user_agent: str = "", ip: str = ""):
    """Envía un evento server-side a GA4 a través de Measurement Protocol"""
    
    # URL de Measurement Protocol
    url = f"https://www.google-analytics.com/mp/collect?api_secret={GA4_API_SECRET}&measurement_id={GA4_MEASUREMENT_ID}"
    
    payload = {
        "client_id": cid or "unknown_user",
        "events": [{
            "name": "clic_correo",
            "params": {
                "campana": campana,
                "plantilla": plantilla,
                "contenido": contenido,
                "destino": destino,
                "medium": "correo",
                "source": "partnertech"
            }
        }]
    }

    headers = {
        "User-Agent": user_agent
    }
    
    # Intenta enviar rápidamente sin bloquear el redreccionamiento prolongadamente
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, headers=headers, timeout=2.0)
    except Exception as e:
        print(f"Error enviando a GA4: {e}")


@app.get("/clic")
async def handle_click(
    request: Request,
    url: str,
    cid: str = "",
    campana: str = "",
    plantilla: str = "",
    contenido: str = ""
):
    """
    Endpoint principal para redirección.
    Recibe los parámetros y los reenvía a GA4 antes de redirigir.
    Ejemplo de uso: /clic?url=https://linkedin.com&cid=123&campana=crm...
    """
    # 1. Recuperar la URL real (unquote por si viene codificada)
    destino = unquote(url)
    
    # 2. Enviar el evento extra a GA4 de forma asíncrona
    user_agent = request.headers.get("user-agent", "")
    ip = request.client.host if request.client else ""
    
    await send_ga4_event(
        cid=cid,
        campana=campana,
        plantilla=plantilla,
        contenido=contenido,
        destino=destino,
        user_agent=user_agent,
        ip=ip
    )
    
    # 3. Redirigir al usuario al destino
    return RedirectResponse(url=destino, status_code=302)

@app.get("/health")
def health_check():
    return {"status": "ok"}
