from random import randint

import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

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


@pytest.mark.anyio
async def test_quiz_exists(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    assert await crud_quiz.exists(db, quiz)


@pytest.mark.anyio
async def test_quiz_not_exists(db: Session) -> None:
    quiz = await get_nonexistent_quiz()
    assert not await crud_quiz.exists(db, quiz)


@pytest.mark.anyio
async def test_create_quiz(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    assert await crud_quiz.exists(db, quiz)
    assert hasattr(quiz, "title")
    assert quiz.title
    assert hasattr(quiz, "description")
    assert quiz.description


@pytest.mark.anyio
async def test_create_quiz_is_active(db: Session) -> None:
    quiz = await create_random_quiz(db=db, is_active=True)
    assert await crud_quiz.exists(db, quiz)
    assert quiz.is_active


@pytest.mark.anyio
async def test_create_quiz_is_active(db: Session) -> None:
    quiz = await create_random_quiz(db=db, is_active=False)
    assert await crud_quiz.exists(db, quiz)
    assert not quiz.is_active


@pytest.mark.anyio
async def test_get_quiz(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    quiz_2 = await crud_quiz.get(db, id=quiz.id)
    assert quiz_2
    assert quiz.title == quiz_2.title
    assert quiz.description == quiz_2.description
    assert jsonable_encoder(quiz) == jsonable_encoder(quiz_2)


@pytest.mark.anyio
async def test_update_quiz(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    new_title = await random_lower_string()
    new_description = await random_lower_string()
    await crud_quiz.update(
        db,
        old_obj=quiz,
        new_obj=QuizCreate(
            title=new_title,
            description=new_description
        )
    )
    quiz_2 = await crud_quiz.get(db, id=quiz.id)
    assert quiz_2
    assert quiz_2.id == quiz.id
    assert quiz_2.title == new_title
    assert quiz_2.description == new_description


@pytest.mark.anyio
async def test_delete_quiz(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    await crud_quiz.delete(db, id=quiz.id)
    assert not await crud_quiz.exists(db, quiz)


@pytest.mark.anyio
async def test_question_exists(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    assert await crud_question.exists(db, question)


@pytest.mark.anyio
async def test_question_not_exists(db: Session) -> None:
    question = await get_nonexistent_question()
    assert not await crud_question.exists(db, question)


@pytest.mark.anyio
async def test_create_question(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    assert await crud_question.exists(db, question)
    assert hasattr(question, "question_text")
    assert question.question_text
    assert hasattr(question, "quiz_id")
    assert question.quiz_id == quiz.id


@pytest.mark.anyio
async def test_get_question(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    question_2 = await crud_question.get(db, id=question.id)
    assert question_2
    assert question.question_text == question_2.question_text
    assert jsonable_encoder(question) == jsonable_encoder(question_2)


@pytest.mark.anyio
async def test_update_question(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    new_question_text = await random_lower_string()
    await crud_question.update(
        db,
        old_obj=question,
        new_obj=QuestionCreate(
            quiz_id=quiz.id,
            question_text=new_question_text
        )
    )
    question_2 = await crud_question.get(db, id=question.id)
    assert question_2
    assert question_2.id == question.id
    assert question_2.question_text == new_question_text


@pytest.mark.anyio
async def test_delete_question(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    await crud_question.delete(db, id=question.id)
    assert not await crud_question.exists(db, question)


@pytest.mark.anyio
async def test_category_exists(db: Session) -> None:
    category = await create_random_category(db=db)
    assert await crud_category.exists(db, category)


@pytest.mark.anyio
async def test_category_not_exists(db: Session) -> None:
    category = await get_nonexistent_category()
    assert not await crud_category.exists(db, category)


@pytest.mark.anyio
async def test_create_category(db: Session) -> None:
    category = await create_random_category(db=db)
    assert await crud_category.exists(db, category)
    assert hasattr(category, "name")
    assert category.name
    assert hasattr(category, "description")
    assert category.description

TEST_USER_SCORE: int = 10

@pytest.mark.anyio
async def test_get_category(db: Session) -> None:
    category = await create_random_category(db=db)
    category_2 = await crud_category.get(db, id=category.id)
    assert category_2
    assert category.name == category_2.name
    assert category.description == category_2.description
    assert jsonable_encoder(category) == jsonable_encoder(category_2)


@pytest.mark.anyio
async def test_update_category(db: Session) -> None:
    category = await create_random_category(db=db)
    new_category_name = await random_lower_string()
    new_category_description = await random_lower_string()
    await crud_category.update(
        db,
        old_obj=category,
        new_obj=CategoryCreate(
            name=new_category_name,
            description=new_category_description
        )
    )
    category_2 = await crud_category.get(db, id=category.id)
    assert category_2
    assert category_2.id == category.id
    assert category_2.name == new_category_name
    assert category_2.description == new_category_description


@pytest.mark.anyio
async def test_delete_category(db: Session) -> None:
    category = await create_random_category(db=db)
    await crud_category.delete(db, id=category.id)
    assert not await crud_category.exists(db, category)


@pytest.mark.anyio
async def test_answer_exists(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    answer = await create_random_answer(db=db, question_id=question.id)
    assert await crud_answer.exists(db, answer)


@pytest.mark.anyio
async def test_answer_not_exists(db: Session) -> None:
    question = await get_nonexistent_answer()
    assert not await crud_answer.exists(db, question)


@pytest.mark.anyio
async def test_create_correct_answer(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    answer = await create_random_answer(db=db, question_id=question.id, is_correct=True)
    assert await crud_answer.exists(db, answer)
    assert answer.question_id == question.id
    assert answer.question.quiz_id == quiz.id
    assert answer.is_correct


@pytest.mark.anyio
async def test_create_incorrect_answer(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    answer = await create_random_answer(db=db, question_id=question.id, is_correct=False)
    assert await crud_answer.exists(db, answer)
    assert answer.question_id == question.id
    assert answer.question.quiz_id == quiz.id
    assert not answer.is_correct


@pytest.mark.anyio
async def test_get_answer(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    answer = await create_random_answer(db=db, question_id=question.id)
    answer_2 = await crud_answer.get(db, id=answer.id)
    assert answer_2
    assert answer_2.id == answer.id
    assert jsonable_encoder(answer_2) == jsonable_encoder(answer)


@pytest.mark.anyio
async def test_update_answer_text(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    answer = await create_random_answer(db=db, question_id=question.id)
    new_answer_text = await random_lower_string()
    await crud_answer.update(
        db,
        old_obj=answer,
        new_obj=AnswerCreate(
            question_id=question.id,
            answer_text=new_answer_text,
            is_correct=answer.is_correct
        )
    )
    answer_2 = await crud_answer.get(db, id=answer.id)
    assert answer_2
    assert answer_2.id == answer.id
    assert answer_2.answer_text == new_answer_text


@pytest.mark.anyio
async def test_delete_answer(db: Session) -> None:
    quiz = await create_random_quiz(db=db)
    question = await create_random_question(db=db, quiz_id=quiz.id)
    answer = await create_random_answer(db=db, question_id=question.id)
    await crud_answer.delete(db, id=answer.id)
    assert not await crud_answer.exists(db, answer)


@pytest.mark.anyio
async def test_create_quiz_result(db: Session) -> None:
    user = await create_random_user(db=db)
    quiz = await create_random_quiz(db=db)
    quiz_result = await create_quiz_result(db=db, user_id=user.id, quiz_id=quiz.id)
    assert quiz_result
    assert quiz_result.user_id == user.id
    assert quiz_result.quiz_id == quiz.id
    assert quiz_result.user_score
    assert quiz_result.max_score


@pytest.mark.anyio
async def test_get_quiz_result(db: Session) -> None:
    user = await create_random_user(db=db)
    quiz = await create_random_quiz(db=db)
    quiz_result = await create_quiz_result(db=db, user_id=user.id, quiz_id=quiz.id)
    quiz_result_2 = await crud_quiz_result.get(db, id=quiz_result.id)
    assert quiz_result_2
    assert quiz_result_2.id == quiz_result.id
    assert jsonable_encoder(quiz_result_2) == jsonable_encoder(quiz_result)


@pytest.mark.anyio
async def test_update_answer_text(db: Session) -> None:
    user = await create_random_user(db=db)
    quiz = await create_random_quiz(db=db)
    quiz_result = await create_quiz_result(db=db, user_id=user.id, quiz_id=quiz.id)
    new_user_score = randint(0, 100)
    new_max_score = new_user_score + randint(0, 100)
    await crud_quiz_result.update(
        db,
        old_obj=quiz_result,
        new_obj=QuizResultCreate(
            user_id=user.id,
            quiz_id=quiz.id,
            user_score=new_user_score,
            max_score=new_max_score
        )
    )
    quiz_result_2 = await crud_quiz_result.get(db, id=quiz_result.id)
    assert quiz_result_2
    assert quiz_result_2.id == quiz_result.id
    assert quiz_result_2.user_score == new_user_score
    assert quiz_result_2.max_score == new_max_score


@pytest.mark.anyio
async def test_delete_answer(db: Session) -> None:
    user = await create_random_user(db=db)
    quiz = await create_random_quiz(db=db)
    quiz_result = await create_quiz_result(db=db, user_id=user.id, quiz_id=quiz.id)
    await crud_quiz_result.delete(db, id=quiz_result.id)
    assert not await crud_quiz_result.get(db, id=quiz_result.id)
