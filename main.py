from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from db.database import Base, engine
import os

from api.routes import router

app = FastAPI(title="Fintech Credit Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

Base.metadata.create_all(bind=engine)

@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse("frontend/index.html")


@app.get("/dashboard", include_in_schema=False)
def serve_dashboard():
    return FileResponse(os.path.join("frontend", "dashboard.html"))