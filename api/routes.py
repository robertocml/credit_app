from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.schemas import ApplicationCreate
from services.scoring_service import get_credit_score
from services.credit_engine import evaluate_application
from repositories.application_repository import create_application, get_application

router = APIRouter()

@router.post("/applications")
def create_new_application(data: ApplicationCreate, db: Session = Depends(get_db)):

    score = get_credit_score()
    status, explanation = evaluate_application(data, score)

    app_dict = data.dict()
    app_dict["credit_score"] = score
    app_dict["status"] = status
    app_dict["explanation"] = explanation

    application = create_application(db, app_dict)

    return application


@router.get("/applications/{application_id}")
def get_application_status(application_id: int, db: Session = Depends(get_db)):

    application = get_application(db, application_id)

    if not application:
        return {"error": "Application not found"}

    return application