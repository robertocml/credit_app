from sqlalchemy import Column, Integer, String, Float, Text
from db.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rfc = Column(String)
    curp = Column(String)
    age = Column(Integer)
    gender = Column(String)
    monthly_income = Column(Float)
    bank_seniority_months = Column(Integer)
    address = Column(String)

    credit_score = Column(Integer)
    status = Column(String)
    explanation = Column(Text)