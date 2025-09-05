from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Configuração do banco
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Time Capsule API")

# Modelo SQLAlchemy
class Capsule(Base):
    __tablename__ = "capsules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)
    send_date = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Schemas Pydantic
class CapsuleCreate(BaseModel):
    name: str
    email: EmailStr
    recipient_name: str
    recipient_email: EmailStr
    send_date: datetime
    message: str

class CapsuleOut(BaseModel):
    id: int
    name: str
    email: str
    recipient_name: str
    recipient_email: str
    send_date: datetime
    message: str

    class Config:
        orm_mode = True

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/")
def read_root():
    return {"msg": "API da cápsula do tempo está rodando!"}

@app.post("/capsule/", response_model=CapsuleOut)
def create_capsule(capsule: CapsuleCreate, db: Session = Depends(get_db)):
    db_capsule = Capsule(
        name=capsule.name,
        email=capsule.email,
        recipient_name=capsule.recipient_name,
        recipient_email=capsule.recipient_email,
        send_date=capsule.send_date,
        message=capsule.message
    )
    db.add(db_capsule)
    db.commit()
    db.refresh(db_capsule)
    return db_capsule

@app.get("/capsule/", response_model=List[CapsuleOut])
def list_capsules(db: Session = Depends(get_db)):
    return db.query(Capsule).all()
