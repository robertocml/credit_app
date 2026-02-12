import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_document_info(file_path: str):

    mime_type = None

    if file_path.lower().endswith(".pdf"):
        mime_type = "application/pdf"
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        mime_type = "image/png"  # Gemini acepta igual aunque sea jpg
    else:
        raise ValueError("Unsupported file type")

    uploaded_file = genai.upload_file(
        file_path,
        mime_type=mime_type
    )

    prompt = """
    Extrae del comprobante:
    - Nombre completo
    - Dirección completa
    - Fecha de vigencia

    Devuelve SOLO un JSON válido con esta estructura:
    {
        "name": "",
        "address": "",
        "valid_date": ""
    }
    """

    response = model.generate_content(
        [uploaded_file, prompt],
        generation_config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)


def validate_address_match(client_address: str, document_address: str):

    prompt = f"""
    ¿Las siguientes dos direcciones corresponden al mismo lugar?

    Dirección del cliente:
    {client_address}

    Dirección del documento:
    {document_address}

    Responde SOLO en formato JSON:
    {{
        "match": true/false,
        "confidence": 0-100
    }}
    """

    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)