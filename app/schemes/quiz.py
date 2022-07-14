from typing import Any
from datetime import datetime
from unicodedata import name

from pydantic import BaseModel, root_validator


# Request model for the quiz questions with user answers

class UserAnswerRequset(BaseModel):
    answer_id: int
    is_correct: bool


class QuizRequset(BaseModel):
    quiz_id: int
    answers: list[UserAnswerRequset]

# Response model for the quiz questions for user to answer

class QuestionAnswerVariantResponse(BaseModel):
    answer_id: int
    answer_text: str


class QuestionResponse(BaseModel):
    question_id: int
    question_text: str
    answer_variants: list[QuestionAnswerVariantResponse]


class QuizResponse(BaseModel):
    quiz_id: int
    quiz_title: str
    quiz_description: str
    questions: list[QuestionResponse]


class QuizResultResponse(BaseModel):
    max_score: int
    user_score: int
    score_percentage: float | None

    @root_validator
    def compute_score_percentage(cls, values) -> dict:
        score_percentage = round(values["user_score"] / values["max_score"]  * 100, 2)
        values["score_percentage"] = score_percentage
        return values

## CRUD

# Create

class QuizCreate(BaseModel):
    title: str
    description: str


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class QuestionCreate(BaseModel):
    quiz_id: int
    question_text: str


class AnswerCreate(BaseModel):
    question_id: int
    answer_text: str
    is_correct: bool

# Retrieve/Update

class QuizScheme(BaseModel):
    id: int
    title: str
    description: str
    is_active: bool = True

    class Config:
        orm_mode = True


class QuestionScheme(BaseModel):
    id: int
    question_text: str
    quiz_id: int
    categories: Any | None = None

    class Config:
        orm_mode = True


class AnswerScheme(BaseModel):
    id: int
    question_id: int
    answer_text: str
    is_correct: bool = False

    class Config:
        orm_mode = True


class CategoryScheme(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        orm_mode = True


class QuizResultScheme(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    max_score: float
    user_score: float
    finished_at: datetime

    class Config:
        orm_mode = True
