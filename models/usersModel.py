from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from cors.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # email = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

