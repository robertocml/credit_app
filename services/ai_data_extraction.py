import os
import json
import mimetypes
from google import genai
from google.genai import types

client = genai.Client()

def extract_document_info(file_path: str):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    prompt = """
    Extrae del comprobante:
    - Nombre completo
    - Dirección completa
    - Fecha de vigencia

    Devuelve un JSON válido con esta estructura:
    {
        "name": "",
        "address": "",
        "valid_date": ""
    }
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        return json.loads(response.text)
    
    except Exception as e:
        print(f"Error en extract_document_info: {e}")
        raise RuntimeError(f"AI extraction failed: {e}")


def validate_address_match(client_address: str, document_address: str):
    prompt = f"""
    ¿Las siguientes dos direcciones corresponden al mismo lugar? 
    Considera abreviaturas y variaciones de escritura.

    Dirección del cliente: {client_address}
    Dirección del documento: {document_address}

    Responde en formato JSON:
    {{
        "match": true/false,
        "confidence": 0-100
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error en validate_address_match: {e}")
        return {"match": False, "confidence": 0}