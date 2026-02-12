from fastapi import FastAPI
from api.routes import router
from db.database import engine
from models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fintech Credit Engine")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Fintech Credit Engine API running"}