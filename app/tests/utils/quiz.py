from sqlalchemy.orm import Session

from app.crud.quiz import (
    crud_quiz,
    crud_question,
    crud_category,
    crud_answer,
    crud_quiz_result
)
from app.database.models.quiz import (
    Quiz,
    Question,
    Category,
    Answer
)
from app.schemes.quiz import (
    QuizCreate,
    QuestionCreate,
    CategoryCreate,
    AnswerCreate,
    QuizResultCreate
)
from app.tests.utils.utils import random_lower_string


async def create_random_quiz(db: Session, is_active: bool = True) -> Quiz:
    return await crud_quiz.create(
        db=db,
        new_obj=QuizCreate(
            title=await random_lower_string(),
            description=await random_lower_string(),
            is_active=is_active
        )
    )


async def get_nonexistent_quiz(is_active: bool = True) -> Quiz:
    return Quiz(
        title=await random_lower_string(),
        description=await random_lower_string(),
        is_active=is_active
    )


async def create_random_question(db: Session, quiz_id: int) -> Question:
    return await crud_question.create(
        db=db,
        new_obj=QuestionCreate(
            quiz_id=quiz_id,
            question_text=await random_lower_string()
        )
    )


async def get_nonexistent_question(nonexistent_quiz_id: int = -1) -> Question:
    return Question(
        question_text=await random_lower_string(),
        quiz_id=nonexistent_quiz_id
    )


async def create_random_category(db: Session) -> Category:
    return await crud_category.create(
        db=db,
        new_obj=CategoryCreate(
            name=await random_lower_string(),
            description=await random_lower_string()
        )
    )


async def get_nonexistent_category() -> Category:
    return Category(
        name=await random_lower_string(),
        description=await random_lower_string()
    )


async def create_random_answer(db: Session, question_id: int, is_correct: bool = False) -> Answer:
    return await crud_answer.create(
        db=db,
        new_obj=AnswerCreate(
            question_id=question_id,
            answer_text=await random_lower_string(),
            is_correct=is_correct
        )
    )


async def get_nonexistent_answer(nonexistent_question_id: int = -1) -> Answer:
    return Answer(
        question_id=nonexistent_question_id,
        answer_text=await random_lower_string()
    )


async def create_quiz_result(db: Session, user_id: int, quiz_id: int, user_score: int = 10, max_score: int = 10) -> Quiz:
    return await crud_quiz_result.create(
        db=db,
        new_obj=QuizResultCreate(
            user_id=user_id,
            quiz_id=quiz_id,
            user_score=user_score,
            max_score=max_score
        )
    )
