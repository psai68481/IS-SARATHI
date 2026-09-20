import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(50), default="government_officer") # government_officer, technical_expert, administrator
    department = Column(String(200), nullable=True) # e.g., PWD, NTPC, NHAI, GeM
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
