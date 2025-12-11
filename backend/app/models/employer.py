from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .user import Base, User
from datetime import datetime

class Employer(Base):
    __tablename__ = 'employers'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    company_name = Column(String(120), nullable=False)
    company_description = Column(Text, nullable=True)
    company_logo_url = Column(String(500), nullable=True)
    company_website = Column(String(255), nullable=True)
    phone = Column(String(15), nullable=True)
    location = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="employer_profile")
    jobs = relationship("Job", back_populates="employer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Employer {self.company_name}>"
