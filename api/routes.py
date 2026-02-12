import os
import shutil
from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi import status as st
from sqlalchemy.orm import Session

from db.database import get_db
from models.models import Application
from schemas.schemas import ApplicationCreate
from services.scoring_service import get_credit_score
from services.credit_engine import evaluate_application
from services.ai_data_extraction import extract_document_info, validate_address_match
from repositories.application_repository import create_application, get_application


router = APIRouter()

@router.post("/applications")
def create_new_application(data: ApplicationCreate,db: Session = Depends(get_db)):

    app_dict = data.dict()
    app_dict["status"] = "PENDIENTE"
    app_dict["credit_score"] = None
    app_dict["explanation"] = None

    application = create_application(db, app_dict)

    return {    
        "id": application.id,
        "status": application.status,
        "message": "Application created successfully. Please upload documents."
    }



@router.post("/applications/{application_id}/documents")
def upload_document(application_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):

    application = get_application(db, application_id)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    try:
        extracted_data = extract_document_info(file_path)
    except Exception as e:
        error_message = str(e)

        if "you exceeded your current quota" in error_message.lower():
            explanation = "No se pudo extraer la información: cuota de Gemini API excedida."
        else:
            explanation = "Error procesando documento. Intenta más tarde. "

        return {
            "status": "PENDING",
            "credit_score": None,
            "explanation": explanation,
            "extracted_data": {}
        }
    try:
        address_validation = validate_address_match(application.address, extracted_data.get("address", ""))
        match = address_validation.get("match", False)
    except Exception as e:
        print("Error validando dirección:", e)
        match = False

    score = get_credit_score()
    status, explanation = evaluate_application("credito_personal", application, score, match)

    application.credit_score = score
    application.status = status
    application.explanation = explanation
    application.address_extracted = extracted_data.get("address")
    application.address_match = match
    application.evaluation_timestamp = datetime.utcnow()
    application.decision_engine_version = "v1.0"

    db.commit()
    db.refresh(application)

    return {
        "message": "Document processed successfully",
        "status": status,
        "credit_score": score,
        "explanation": explanation,
        "extracted_data": extracted_data
    }


@router.get("/applications/{application_id}")
def get_application_status(application_id: int, db: Session = Depends(get_db)):

    application = get_application(db, application_id)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return {
        "id": application.id,
        "status": application.status
    }

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    total = db.query(Application).count()
    approved = db.query(Application).filter(Application.status == "APROBADO").count()
    rejected = db.query(Application).filter(Application.status == "RECHAZADO").count()
    pending = db.query(Application).filter(Application.status == "PENDIENTE").count()

    approval_rate = round((approved / total) * 100, 2) if total else 0

    return {
        "total": total,
        "approved": approved,
        "rejected": rejected,
        "pending": pending,
        "approval_rate_percent": approval_rate
    }

@router.get("/scorecredito")
def get_score(id: int):
    score = get_credit_score()
    
    return {
        "id": id,
        "score": score
    }
