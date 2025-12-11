from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from .user import Base
from datetime import datetime
import enum

class ApplicationStatus(enum.Enum):
    APPLIED = "applied"
    REVIEWED = "reviewed"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    job_seeker_id = Column(Integer, ForeignKey('job_seekers.id'), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, index=True)
    cover_letter = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)  # Employer notes
    applied_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    job_seeker = relationship("JobSeeker", back_populates="applications")
    
    def __repr__(self):
        return f"<Application Job:{self.job_id} Seeker:{self.job_seeker_id} - {self.status.value}>"
