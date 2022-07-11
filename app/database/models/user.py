from sqlalchemy import (
    Boolean,
    DateTime,
    Column,
    Integer,
    String
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.database.session import engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    quiz_results = relationship("QuizResults", back_populates="user")

Base.metadata.create_all(engine)
