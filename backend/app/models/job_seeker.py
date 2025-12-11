from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .user import Base, User
from datetime import datetime

class JobSeeker(Base):
    __tablename__ = 'job_seekers'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    skills = Column(Text, nullable=True)  # JSON format: "Python, JavaScript, React"
    experience_years = Column(Integer, default=0)
    cv_url = Column(String(500), nullable=True)
    phone = Column(String(15), nullable=True)
    location = Column(String(120), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="job_seeker_profile")
    applications = relationship("Application", back_populates="job_seeker", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<JobSeeker {self.user.email}>"
