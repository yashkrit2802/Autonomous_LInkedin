from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    linkedin_urn = Column(String, unique=True, index=True)
    access_token = Column(String, nullable=False)
    # The agent will use this data for personal branding
    persona_data = Column(String) 
    industry = Column(String)

    calendar_entries = relationship("ContentCalendar", back_populates="user")
    performance_metrics = relationship("PostPerformance", back_populates="user")

class ContentCalendar(Base):
    __tablename__ = 'content_calendar'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_content = Column(String, nullable=False)
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=False)

    user = relationship("User", back_populates="calendar_entries")

class PostPerformance(Base):
    __tablename__ = 'post_performance'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(String, unique=True) # LinkedIn post ID
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    
    user = relationship("User", back_populates="performance_metrics")