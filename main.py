import os
import json
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import httpx

app = FastAPI(title="MY-PDF")
templates = Jinja2Templates(directory="templates")

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
OPENAI_BASE_URL = "https://api.openai.com/v1"

async def call_openai_api(prompt: str, system_message: str | None = None) -> str:
    """
    Call OpenAI API with the given prompt and return the response.
    Uses gpt-5 as the newest OpenAI model (released August 7, 2025).
    Do not change this unless explicitly requested by the user.
    """
    # Vérifier si la clé API est valide
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        raise HTTPException(
            status_code=400, 
            detail="Clé API OpenAI manquante. Veuillez configurer votre clé API OpenAI pour utiliser les fonctionnalités IA."
        )
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    
    data = {
        "model": "gpt-3.5-turbo",  # Using gpt-3.5-turbo for better compatibility
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 401:
                raise HTTPException(
                    status_code=400,
                    detail="Clé API OpenAI invalide. Veuillez vérifier votre clé API."
                )
            elif response.status_code == 429:
                raise HTTPException(
                    status_code=400,
                    detail="Limite de requêtes atteinte. Votre clé API OpenAI a épuisé son quota ou ses crédits. Vérifiez votre compte OpenAI ou attendez avant de réessayer."
                )
            elif response.status_code == 402:
                raise HTTPException(
                    status_code=400,
                    detail="Quota épuisé. Votre clé API OpenAI n'a plus de crédit. Ajoutez du crédit à votre compte OpenAI."
                )
            elif response.status_code != 200:
                error_detail = f"Erreur API OpenAI (Code {response.status_code})"
                try:
                    error_json = response.json()
                    if "error" in error_json and "message" in error_json["error"]:
                        error_detail += f": {error_json['error']['message']}"
                except:
                    error_detail += f": {response.text[:200]}"
                raise HTTPException(
                    status_code=response.status_code,
                    detail=error_detail
                )
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Timeout lors de l'appel à l'API OpenAI")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/corriger")
async def corriger_texte(text: str = Form(...)):
    """
    Correct spelling and grammar errors in the provided text
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide")
    
    system_message = """Tu es un correcteur professionnel de langue française. 
    Corrige uniquement les fautes d'orthographe, de grammaire, de conjugaison et de ponctuation.
    Conserve le style, le ton et la structure du texte original.
    Ne modifie pas le sens ni n'ajoute de contenu."""
    
    prompt = f"Corrige ce texte en français :\n\n{text}"
    
    try:
        corrected_text = await call_openai_api(prompt, system_message)
        return JSONResponse(content={"text": corrected_text})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la correction: {str(e)}")

@app.post("/resumer")
async def resumer_texte(text: str = Form(...)):
    """
    Generate a summary of the provided text
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide")
    
    system_message = """Tu es un expert en résumé de textes.
    Crée un résumé concis et pertinent qui capture les points clés et les idées principales.
    Le résumé doit être significativement plus court que le texte original tout en conservant l'essentiel."""
    
    prompt = f"Résume ce texte en français de manière claire et concise :\n\n{text}"
    
    try:
        summary = await call_openai_api(prompt, system_message)
        return JSONResponse(content={"text": summary})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du résumé: {str(e)}")

@app.post("/organiser")
async def organiser_texte(text: str = Form(...)):
    """
    Reorganize and format the provided text beautifully
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide")
    
    system_message = """Tu es un expert en organisation et mise en forme de textes.
    Réorganise le texte de manière claire et structurée avec :
    - Une structure logique avec titres et sous-titres si approprié
    - Des paragraphes bien délimités
    - Une présentation professionnelle et lisible
    - Conservation du contenu original sans ajout d'informations"""
    
    prompt = f"Réorganise et formate joliment ce texte en français :\n\n{text}"
    
    try:
        organized_text = await call_openai_api(prompt, system_message)
        return JSONResponse(content={"text": organized_text})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'organisation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
