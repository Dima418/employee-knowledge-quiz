"""Quiz pydantic schemes.

"""

from pydantic import BaseModel, root_validator


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


class QuizResultResponse(BaseModel):
    max_score: int
    user_score: int
    score_percentage: float | None

    @root_validator
    def compute_score_percentage(cls, values) -> dict:
        score_percentage = values["user_score"] / values["max_score"] * 100
        values["score_percentage"] = score_percentage
        return values
