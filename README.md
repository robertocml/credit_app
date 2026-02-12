## 🧠 Fintech Credit Engine — Prueba Técnica

## URL Railway:  https://creditapp-production.up.railway.app/

API REST para gestionar solicitudes de crédito personal digital:

- Crear solicitudes (`POST /applications`)
- Subir comprobante de domicilio (`POST /applications/{id}/documents`)
- Extraer datos del comprobante con IA (Google Gemini)
- Evaluar crédito con reglas de negocio
- Consultar estado y obtener score
- Dashboard de métricas

---

## 🚀 Endpoints principales

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/applications` | POST | Crear nueva solicitud |
| `/applications/{id}/documents` | POST | Subir comprobante y evaluar |
| `/applications/{id}` | GET | Consultar estado |
| `/applications/{id}/scorecredit` | GET | Obtener solo el credit score |
| `/metrics` | GET | Métricas de solicitudes |

---

## ⚙️ Cómo ejecutar

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/credit_app.git
   cd credit_app

2.	Crea entorno virtual e instala dependencias:
    ```bash
    python -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate      # Windows
    pip install -r requirements.txt


3.	Variables de entorno:
    ```bash
    export GEMINI_API_KEY="TU_API_KEY_DE_GEMINI"
    export DATABASE_URL="sqlite:///./credit.db"

4.	Inicia el servidor:
    uvicorn main:app --reload