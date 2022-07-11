from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.database.models.user import User


# Request model for the quiz questions with user answers

class QuizRequset(BaseModel):
    quiz_id: int
    answers: list["UserAnswer"]


class UserAnswer(BaseModel):
    quiz_id: int
    answers: list[bool]


# Response model for the quiz questions for user to answer

class QuizResponse(BaseModel):
    quiz_id: int
    quiz_title: str
    quiz_description: str
    quesions: list["Question"]


class Question(BaseModel):
    question_id: int
    question_text: str
    answer_variants: list["AnswerVariant"]


class AnswerVariant(BaseModel):
    answer_id: int
    answer_text: str


# Schemes for CRUD

class Quiz(BaseModel):
    id: int
    title: str
    description: str
    is_active: bool = True

    class Config:
        orm_mode = True


class Question(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    categories: Any | None = None

    class Config:
        orm_mode = True


class Answer(BaseModel):
    question_id: int
    answer_text: str
    is_correct: bool = False

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class QuizResult(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    score: float = 0
    finished_at: datetime

    class Config:
        orm_mode = True
