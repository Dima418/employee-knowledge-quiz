from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.database.session import engine


# Many-to-many relationship between Category and Question
questions_categories = Table(
    "questions_categories",
    Base.metadata,
    Column("question_id", ForeignKey("questions.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # one-to-many relationship with Question
    questions = relationship("Question", back_populates="quiz")

    # one-to-many relationship with QuizResult
    quiz_results = relationship("QuizResult", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)

    # bidirectional one-to-many relationship with Quiz
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    quiz = relationship("Quiz", back_populates="questions")

    # many-to-many relationship with Category
    categories = relationship("Category", secondary=questions_categories, back_populates="questions")

    # one-to-many relationship with Answer
    answers = relationship("Answer", back_populates="question")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True, default=None)

    # many-to-many relationship with Question
    questions = relationship("Question", secondary=questions_categories, back_populates="categories")


class Answer(Base):
    __tablename__ = "answers"
    answer_text = Column(String, primary_key=True)
    is_correct = Column(Boolean, default=False, primary_key=True)

    # bidirectional one-to-many relationship with Question
    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    question = relationship("Question", back_populates="answers")


class QuizResults(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False, default=0)
    finished_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # bidirectional one-to-many relationship with Question
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="quiz_results")

    # bidirectional one-to-manyrelationship with Question
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    quiz = relationship("Quiz", back_populates="quiz_results")

Base.metadata.create_all(engine)
