from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    name: str
    rfc: str
    curp: str
    age: int
    gender: str
    monthly_income: float
    bank_seniority_months: int
    address: str

class ApplicationResponse(ApplicationCreate):
    id: int
    credit_score: int
    status: str
    explanation: str

    class Config:
        from_attributes = True