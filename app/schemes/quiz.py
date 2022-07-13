"""Quiz pydantic schemes.

"""

from datetime import datetime

from pydantic import BaseModel


# Request model for the quiz questions with user answers

class UserAnswerRequset(BaseModel):
    answer_id: int
    is_correct: bool


class QuestionRequset(BaseModel):
    question_id: int
    user_answers: list[UserAnswerRequset]


class QuizRequset(BaseModel):
    quiz_id: int
    questions: list[QuestionRequset]

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

# Schemes for CRUD

class QuizScheme(BaseModel):
    id: int
    title: str
    description: str
    is_active: bool = True

    class Config:
        orm_mode = True


class CategoryScheme(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        orm_mode = True


class QuestionScheme(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    categories: list[CategoryScheme] | None = None

    class Config:
        orm_mode = True


class AnswerScheme(BaseModel):
    id: int
    question_id: int
    answer_text: str
    is_correct: bool = False

    class Config:
        orm_mode = True


class QuizResultScheme(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    user_score: float = 0
    max_score: float = 0
    finished_at: datetime

    class Config:
        orm_mode = True
