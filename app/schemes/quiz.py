from typing import Any
from datetime import datetime
from unicodedata import name

from pydantic import BaseModel, root_validator


class UserAnswerRequset(BaseModel):
    answer_id: int
    is_correct: bool


class QuizRequset(BaseModel):
    quiz_id: int
    answers: list[UserAnswerRequset]


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


class QuizCreate(BaseModel):
    title: str
    description: str
    is_active: bool | None = True


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


class QuizResultCreate(BaseModel):
    user_id: int
    quiz_id: int
    user_score: int = 0
    max_score: int = 1


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
