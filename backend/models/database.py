"""
Database models and initialization
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    """User model for storing user profiles"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=True)
    email = Column(String(120), unique=True, nullable=True)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    preferences = Column(Text)  # JSON stored as text

class UserMeasurements(Base):
    """Store encrypted user body measurements"""
    __tablename__ = 'user_measurements'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    chest_cm = Column(Float)
    waist_cm = Column(Float)
    hip_cm = Column(Float)
    shoulder_width_cm = Column(Float)
    body_type = Column(String(50))
    size_preference = Column(String(20))  # 'loose', 'fitted', 'regular'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Avatar(Base):
    """Store user avatar information"""
    __tablename__ = 'avatars'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    avatar_data = Column(Text)  # Encrypted avatar configuration
    image_path = Column(String(255))  # Encrypted path to avatar image
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatHistory(Base):
    """Store chat conversation history"""
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(String(100))
    message_type = Column(String(20))  # 'user' or 'bot'
    message = Column(Text)
    message_metadata = Column(Text)  # JSON for additional data
    created_at = Column(DateTime, default=datetime.utcnow)

class TryOnHistory(Base):
    """Store virtual try-on history"""
    __tablename__ = 'tryon_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_url = Column(String(500))
    product_name = Column(String(255))
    result_image_path = Column(String(255))
    rating = Column(Integer)  # User rating 1-5
    created_at = Column(DateTime, default=datetime.utcnow)

class SavedOutfits(Base):
    """Store user's saved outfit combinations"""
    __tablename__ = 'saved_outfits'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    outfit_name = Column(String(255))
    items = Column(Text)  # JSON array of product URLs/IDs
    occasion = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database engine and session
engine = None
SessionLocal = None

def init_db():
    """Initialize database"""
    global engine, SessionLocal
    
    database_url = os.getenv('DATABASE_URL', 'sqlite:///fashion_chatbot.db')
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("Database initialized successfully")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def close_db(db):
    """Close database session"""
    if db:
        db.close()
