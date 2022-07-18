from random import randint

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database.models.quiz import (
    Quiz,
    Question,
    Category,
    Answer,
    QuizResult
)
from app.crud.quiz import (
    crud_quiz,
    crud_question,
    crud_category,
    crud_answer,
    crud_quiz_result
)
from app.schemes.quiz import (
    QuizCreate,
    QuestionCreate,
    CategoryCreate,
    AnswerCreate,
    QuizResultCreate
)
from app.tests.utils.quiz import (
    create_random_quiz,
    create_random_question,
    create_random_category,
    create_random_answer,
    create_quiz_result,
    get_nonexistent_quiz,
    get_nonexistent_question,
    get_nonexistent_category,
    get_nonexistent_answer
)
from app.tests.utils.utils import random_lower_string
from app.tests.utils.user import create_random_user


async def test_quiz_exists(db: Session, new_active_quiz: Quiz) -> None:
    assert await crud_quiz.exists(db, new_active_quiz)


async def test_quiz_not_exists(db: Session, nonexistent_quiz: Quiz) -> None:
    assert not await crud_quiz.exists(db, nonexistent_quiz)


async def test_create_quiz(db: Session, new_active_quiz: Quiz) -> None:
    assert await crud_quiz.exists(db, new_active_quiz)
    assert hasattr(new_active_quiz, "title")
    assert new_active_quiz.title
    assert hasattr(new_active_quiz, "description")
    assert new_active_quiz.description



async def test_create_quiz_is_active(db: Session, new_active_quiz: Quiz) -> None:
    assert await crud_quiz.exists(db, new_active_quiz)
    assert new_active_quiz.is_active


async def test_create_quiz_is_active(db: Session, new_inactive_quiz: Quiz) -> None:
    assert await crud_quiz.exists(db, new_inactive_quiz)
    assert not new_inactive_quiz.is_active


async def test_get_quiz(db: Session, new_active_quiz: Quiz) -> None:
    same_quiz = await crud_quiz.get(db, id=new_active_quiz.id)
    assert same_quiz
    assert new_active_quiz.title == same_quiz.title
    assert new_active_quiz.description == same_quiz.description
    assert jsonable_encoder(new_active_quiz) == jsonable_encoder(same_quiz)


async def test_update_quiz_title_and_description(db: Session, new_active_quiz: Quiz) -> None:
    new_title = await random_lower_string()
    new_description = await random_lower_string()
    await crud_quiz.update(
        db,
        old_obj=new_active_quiz,
        new_obj=QuizCreate(
            title=new_title,
            description=new_description
        )
    )
    same_quiz = await crud_quiz.get(db, id=new_active_quiz.id)
    assert same_quiz
    assert same_quiz.id == new_active_quiz.id
    assert same_quiz.title == new_title
    assert same_quiz.description == new_description


async def test_delete_quiz(db: Session, new_active_quiz: Quiz) -> None:
    await crud_quiz.delete(db, id=new_active_quiz.id)
    assert not await crud_quiz.exists(db, new_active_quiz)


async def test_question_exists(db: Session, new_question: Question) -> None:
    assert await crud_question.exists(db, new_question)


async def test_question_not_exists(db: Session, nonexistent_question: Question) -> None:
    assert not await crud_question.exists(db, nonexistent_question)


async def test_create_question(db: Session, new_question: Question) -> None:
    assert await crud_question.exists(db, new_question)
    assert hasattr(new_question, "question_text")
    assert new_question.question_text
    assert hasattr(new_question, "quiz_id")
    assert new_question.quiz_id


async def test_get_question(db: Session, new_question: Question) -> None:
    same_question = await crud_question.get(db, id=new_question.id)
    assert same_question
    assert new_question.question_text == same_question.question_text
    assert jsonable_encoder(new_question) == jsonable_encoder(same_question)


async def test_update_question_text(db: Session, new_question: Question) -> None:
    new_question_text = await random_lower_string()
    await crud_question.update(
        db,
        old_obj=new_question,
        new_obj=QuestionCreate(
            quiz_id=new_question.quiz_id,
            question_text=new_question_text
        )
    )
    same_question = await crud_question.get(db, id=new_question.id)
    assert same_question
    assert same_question.id == new_question.id
    assert same_question.question_text == new_question_text


async def test_delete_question(db: Session, new_question: Question) -> None:
    await crud_question.delete(db, id=new_question.id)
    assert not await crud_question.exists(db, new_question)


async def test_category_exists(db: Session, new_category: Category) -> None:
    assert await crud_category.exists(db, new_category)


async def test_category_not_exists(db: Session, nonexistent_category: Category) -> None:
    assert not await crud_category.exists(db, nonexistent_category)


async def test_create_category(db: Session, new_category: Category) -> None:
    assert await crud_category.exists(db, new_category)
    assert hasattr(new_category, "name")
    assert new_category.name
    assert hasattr(new_category, "description")
    assert new_category.description


async def test_get_category(db: Session, new_category: Category) -> None:
    same_category = await crud_category.get(db, id=new_category.id)
    assert same_category
    assert new_category.name == same_category.name
    assert new_category.description == same_category.description
    assert jsonable_encoder(new_category) == jsonable_encoder(same_category)


async def test_update_category(db: Session, new_category: Category) -> None:
    new_category_name = await random_lower_string()
    new_category_description = await random_lower_string()
    await crud_category.update(
        db,
        old_obj=new_category,
        new_obj=CategoryCreate(
            name=new_category_name,
            description=new_category_description
        )
    )
    same_category = await crud_category.get(db, id=new_category.id)
    assert same_category
    assert same_category.id == new_category.id
    assert same_category.name == new_category_name
    assert same_category.description == new_category_description


async def test_delete_category(db: Session, new_category: Category) -> None:
    await crud_category.delete(db, id=new_category.id)
    assert not await crud_category.exists(db, new_category)


async def test_answer_exists(db: Session, new_correct_answer: Answer) -> None:
    assert await crud_answer.exists(db, new_correct_answer)


async def test_answer_not_exists(db: Session, nonexistent_answer: Answer) -> None:
    assert not await crud_answer.exists(db, nonexistent_answer)


async def test_create_correct_answer(db: Session, new_correct_answer: Answer) -> None:
    assert await crud_answer.exists(db, new_correct_answer)
    assert new_correct_answer.is_correct


async def test_create_incorrect_answer(db: Session, new_incorrect_answer: Answer) -> None:
    assert await crud_answer.exists(db, new_incorrect_answer)
    assert not new_incorrect_answer.is_correct


async def test_get_answer(db: Session, new_correct_answer: Answer) -> None:
    same_answer = await crud_answer.get(db, id=new_correct_answer.id)
    assert same_answer
    assert same_answer.id == new_correct_answer.id
    assert jsonable_encoder(same_answer) == jsonable_encoder(new_correct_answer)


async def test_update_answer_text(db: Session, new_correct_answer: Answer) -> None:
    new_answer_text = await random_lower_string()
    await crud_answer.update(
        db,
        old_obj=new_correct_answer,
        new_obj=AnswerCreate(
            question_id=new_correct_answer.question_id,
            answer_text=new_answer_text,
            is_correct=new_correct_answer.is_correct
        )
    )
    same_answer = await crud_answer.get(db, id=new_correct_answer.id)
    assert same_answer
    assert same_answer.id == new_correct_answer.id
    assert same_answer.answer_text == new_answer_text


async def test_delete_answer(db: Session, new_correct_answer: Answer) -> None:
    await crud_answer.delete(db, id=new_correct_answer.id)
    assert not await crud_answer.exists(db, new_correct_answer)


async def test_create_quiz_result(db: Session, new_quiz_result: QuizResult) -> None:
    assert new_quiz_result
    assert new_quiz_result.user_id
    assert new_quiz_result.quiz_id
    assert new_quiz_result.user_score
    assert new_quiz_result.max_score


async def test_get_quiz_result(db: Session, new_quiz_result: QuizResult) -> None:
    same_quiz_result = await crud_quiz_result.get(db, id=new_quiz_result.id)
    assert same_quiz_result
    assert same_quiz_result.id == new_quiz_result.id
    assert jsonable_encoder(same_quiz_result) == jsonable_encoder(new_quiz_result)


async def test_update_answer_text(db: Session, new_quiz_result: QuizResult) -> None:
    new_user_score = randint(0, 100)
    new_max_score = new_user_score + randint(0, 100)
    await crud_quiz_result.update(
        db,
        old_obj=new_quiz_result,
        new_obj=QuizResultCreate(
            user_id=new_quiz_result.user_id,
            quiz_id=new_quiz_result.quiz_id,
            user_score=new_user_score,
            max_score=new_max_score
        )
    )
    same_quiz_result = await crud_quiz_result.get(db, id=new_quiz_result.id)
    assert same_quiz_result
    assert same_quiz_result.id == new_quiz_result.id
    assert same_quiz_result.user_score == new_user_score
    assert same_quiz_result.max_score == new_max_score


async def test_delete_answer(db: Session, new_quiz_result: QuizResult) -> None:
    await crud_quiz_result.delete(db, id=new_quiz_result.id)
    assert not await crud_quiz_result.get(db, id=new_quiz_result.id)
