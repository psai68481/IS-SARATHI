import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class HumanDecision(Base):
    __tablename__ = "human_decisions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    department = Column(String(200), nullable=True)
    tender_query = Column(Text, nullable=False)
    
    ai_recommendation = Column(String(100), nullable=False)
    ai_confidence = Column(Float, nullable=False)
    
    human_decision = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    validation_status = Column(String(50), default="Validated") # Validated, Unverified, Rejected
    
    officer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    officer = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False) # SEARCH, RECOMMENDATION, OVERRIDE, EXPORT_REPORT, ADMIN_UPDATE
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
