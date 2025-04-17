from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # ✅ 추가된 필드
    name = Column(String)
    phone_number = Column(String)

    fat_histories = relationship("FatHistory", back_populates="user")

class FatHistory(Base):
    __tablename__ = "fat_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fat_rate = Column(String)
    confidence = Column(Float)
    recommended_diet = Column(String)
    recommended_workout = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="fat_histories")