from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from sqlalchemy.orm import Relationship
from cors.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    blogs = Relationship("Blog", back_populates="creator")
