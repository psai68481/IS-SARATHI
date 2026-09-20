import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Standard(Base):
    __tablename__ = "standards"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    is_number = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(Text, nullable=False, index=True)
    title_ml = Column(Text, nullable=True)  # Native-language title (Hindi/Telugu) for multilingual matching
    scope = Column(Text, nullable=False)
    ics_code = Column(String(50), nullable=True, index=True)
    category = Column(String(150), nullable=True, index=True)
    
    # Version & Status
    status = Column(String(50), default="CURRENT") # CURRENT, REAFFIRMED, SUPERSEDED, WITHDRAWN
    revision_year = Column(Integer, nullable=True)
    latest_version = Column(String(150), nullable=True)
    amendment = Column(Text, nullable=True)

    # Generic applicability metadata (structured, dataset-driven — not just title/keywords)
    exclusions = Column(Text, nullable=True)             # explicit product exclusions from the standard's scope clause
    product_type = Column(String(200), nullable=True)    # normalized product family the standard covers
    technical_keywords = Column(String(500), nullable=True)  # comma-separated technical vocabulary of the standard
    verification_status = Column(String(50), default="VERIFIED")  # VERIFIED | PARTIALLY_VERIFIED | UNVERIFIED
    
    # Certification / BIS Quality Control Order (QCO)
    certification_required = Column(Boolean, default=False)
    certification_scheme = Column(String(100), nullable=True) # BIS ISI Mark, Compulsory Registration Scheme (CRS), Hallmarking
    certification_status = Column(String(50), default="Voluntary") # Mandatory, Voluntary
    qco_notification_number = Column(String(150), nullable=True)
    
    # Document storage reference
    s3_document_key = Column(String(255), nullable=True)
    source_url = Column(Text, nullable=True)
    verified_at = Column(DateTime, default=datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    relationships_from = relationship(
        "StandardRelationship",
        foreign_keys="StandardRelationship.from_standard_id",
        back_populates="from_standard",
        cascade="all, delete-orphan"
    )
    relationships_to = relationship(
        "StandardRelationship",
        foreign_keys="StandardRelationship.to_standard_id",
        back_populates="to_standard",
        cascade="all, delete-orphan"
    )
    clauses = relationship(
        "StandardClause",
        back_populates="standard",
        cascade="all, delete-orphan"
    )

class StandardRelationship(Base):
    __tablename__ = "standard_relationships"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    from_standard_id = Column(String(36), ForeignKey("standards.id", ondelete="CASCADE"), nullable=False)
    to_standard_id = Column(String(36), ForeignKey("standards.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String(50), nullable=False) # normative, test_method, safety, material, installation, terminology
    description = Column(Text, nullable=True)

    from_standard = relationship("Standard", foreign_keys=[from_standard_id], back_populates="relationships_from")
    to_standard = relationship("Standard", foreign_keys=[to_standard_id], back_populates="relationships_to")

class StandardClause(Base):
    __tablename__ = "standard_clauses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    standard_id = Column(String(36), ForeignKey("standards.id", ondelete="CASCADE"), nullable=False)
    clause_number = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    requirement_text = Column(Text, nullable=True)
    tested_parameter = Column(String(150), nullable=True)
    test_limit = Column(String(150), nullable=True)

    standard = relationship("Standard", back_populates="clauses")
