from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    

# this links reviews to user using email 
class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True)
    user_email = Column(String, index=True)
    file_name = Column(String)
    review_type = Column(String)
    result_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)