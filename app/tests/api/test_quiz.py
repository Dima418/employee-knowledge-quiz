from datetime import datetime

from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.database.models.user import User
from app.database.models.quiz import (
    Quiz,
    Question,
    Category,
    Answer,
    QuizResult
)
from app.tests.utils.quiz import (
    create_random_quiz,
    create_random_question,
    create_random_category,
    create_random_answer,
    create_quiz_result
)
from app.schemes.quiz import (
    QuizCreate,
    QuestionCreate,
    CategoryCreate,
    AnswerCreate,
    QuizScheme,
    QuestionScheme,
    CategoryScheme,
    AnswerScheme
)
from app.tests.utils.utils import random_lower_string


async def test_view_quiz(client: AsyncClient, normal_user_token_headers: dict[str: str], new_active_quiz: Quiz) -> None:
    response = await client.get(f"/quiz/{new_active_quiz.id}/view", headers=await normal_user_token_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["quiz_id"] == new_active_quiz.id
    assert response_data["quiz_title"] == new_active_quiz.title
    assert response_data["quiz_description"] == new_active_quiz.description
    assert "questions" in response_data


async def test_submit_quiz(db: Session, client: AsyncClient, normal_user_token_headers: dict[str: str]):
    quiz = await create_random_quiz(db, is_active=True)
    question_1 = await create_random_question(db, quiz.id)
    question_2 = await create_random_question(db, quiz.id)
    asnwer_1_1 = await create_random_answer(db, question_1.id, is_correct=True)
    asnwer_1_2 = await create_random_answer(db, question_1.id, is_correct=False)
    asnwer_1_3 = await create_random_answer(db, question_1.id, is_correct=True)
    asnwer_2_1 = await create_random_answer(db, question_2.id, is_correct=False)
    asnwer_2_2 = await create_random_answer(db, question_2.id, is_correct=True)
    user_ansewers = {
        "quiz_id": quiz.id,
        "answers": [
            {"answer_id": asnwer_1_1.id, "is_correct": True},
            {"answer_id": asnwer_1_2.id, "is_correct": True},
            {"answer_id": asnwer_1_3.id, "is_correct": True},
            {"answer_id": asnwer_2_1.id, "is_correct": True},
            {"answer_id": asnwer_2_2.id, "is_correct": True},
        ]
    }
    response = await client.post(
        f"/quiz/{quiz.id}/submit",
        headers=await normal_user_token_headers,
        json=user_ansewers
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["max_score"] == 5
    assert response_data["user_score"] == 3
    assert response_data["score_percentage"] == 60


async def test_create_quiz(client: AsyncClient, superuser_token_headers: dict[str: str]) -> None:
    new_quiz = QuizCreate(title=await random_lower_string(), description=await random_lower_string())
    response = await client.post("/quiz", headers=await superuser_token_headers, json=new_quiz.dict())
    assert response.status_code == 201


async def test_get_quizzes(db: Session, client: AsyncClient, superuser_token_headers: dict[str: str]) -> None:
    await create_random_quiz(db)
    await create_random_quiz(db)
    await create_random_quiz(db)
    response = await client.get("/quizzes", headers=await superuser_token_headers)
    assert response.status_code == 200
    assert len(response.json()) > 1


async def test_get_quiz(client: AsyncClient, superuser_token_headers: dict[str: str], new_active_quiz: Quiz):
    response = await client.get(f"/quiz/{new_active_quiz.id}", headers=await superuser_token_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_active_quiz.id
    assert response_data["title"] == new_active_quiz.title
    assert response_data["description"] == new_active_quiz.description


async def test_update_quiz(client: AsyncClient, superuser_token_headers: dict[str: str], new_active_quiz: Quiz):
    update_quiz = QuizScheme(
        id=new_active_quiz.id,
        title=await random_lower_string(),
        description=await random_lower_string(),
        is_active=True
    )
    response = await client.patch(
        f"/quiz/{new_active_quiz.id}",
        headers=await superuser_token_headers,
        json=update_quiz.dict()
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_active_quiz.id
    assert response_data["title"] == update_quiz.title
    assert response_data["description"] == update_quiz.description


async def test_delete_quiz(client: AsyncClient, superuser_token_headers: dict[str: str], new_active_quiz: Quiz):
    response = await client.delete(f"/quiz/{new_active_quiz.id}", headers=await superuser_token_headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == new_active_quiz.id
    assert response_data["title"] == new_active_quiz.title
    assert response_data["description"] == new_active_quiz.description


async def test_create_question(client: AsyncClient, superuser_token_headers: dict[str: str], new_active_quiz: Quiz):
    new_question = QuestionCreate(quiz_id=new_active_quiz.id, question_text=await random_lower_string())
    response = await client.post("/question", headers=await superuser_token_headers, json=new_question.dict())
    assert response.status_code == 201


async def test_get_questions(db: Session, client: AsyncClient, superuser_token_headers: dict[str: str], new_active_quiz: Quiz):
    await create_random_question(db, new_active_quiz.id)
    await create_random_question(db, new_active_quiz.id)
    await create_random_question(db, new_active_quiz.id)
    response = await client.get("/questions", headers=await superuser_token_headers)
    assert response.status_code == 200
    assert len(response.json()) > 1


async def test_get_question(client: AsyncClient, superuser_token_headers: dict[str: str], new_question: Question):
    response = await client.get(f"/question/{new_question.id}", headers=await superuser_token_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_question.id
    assert response_data["quiz_id"] == new_question.quiz_id
    assert response_data["question_text"] == new_question.question_text


async def test_update_question(client: AsyncClient, superuser_token_headers: dict[str: str], new_question: Question):
    update_question = QuestionScheme(
        id=new_question.id,
        quiz_id=new_question.quiz_id,
        question_text=await random_lower_string()
    )
    response = await client.patch(
        f"/question/{new_question.id}",
        headers=await superuser_token_headers,
        json=update_question.dict()
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_question.id
    assert response_data["quiz_id"] == update_question.quiz_id
    assert response_data["question_text"] == update_question.question_text


async def test_delete_question(client: AsyncClient, superuser_token_headers: dict[str: str], new_question: Question):
    response = await client.delete(f"/question/{new_question.id}", headers=await superuser_token_headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == new_question.id
    assert response_data["quiz_id"] == new_question.quiz_id
    assert response_data["question_text"] == new_question.question_text


async def test_create_category(client: AsyncClient, superuser_token_headers: dict[str: str]):
    new_category = CategoryCreate(name=await random_lower_string(), description=await random_lower_string())
    response = await client.post("/category", headers=await superuser_token_headers, json=new_category.dict())
    assert response.status_code == 201


async def test_get_categories(db: Session, client: AsyncClient, superuser_token_headers: dict[str: str]):
    await create_random_category(db)
    await create_random_category(db)
    await create_random_category(db)
    response = await client.get("/categories", headers=await superuser_token_headers)
    assert response.status_code == 200
    assert len(response.json()) > 1


async def test_get_category(client: AsyncClient, superuser_token_headers: dict[str: str], new_category: Category):
    response = await client.get(f"/category/{new_category.id}", headers=await superuser_token_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_category.id
    assert response_data["name"] == new_category.name
    assert response_data["description"] == new_category.description


async def test_update_category(client: AsyncClient, superuser_token_headers: dict[str: str], new_category: Category):
    update_category = CategoryScheme(
        id=new_category.id,
        name=await random_lower_string(),
        description=await random_lower_string()
    )
    response = await client.patch(
        f"/category/{new_category.id}",
        headers=await superuser_token_headers,
        json=update_category.dict()
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_category.id
    assert response_data["name"] == update_category.name
    assert response_data["description"] == update_category.description


async def test_delete_category(client: AsyncClient, superuser_token_headers: dict[str: str], new_category: Category):
    response = await client.delete(f"/category/{new_category.id}", headers=await superuser_token_headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == new_category.id
    assert response_data["name"] == new_category.name
    assert response_data["description"] == new_category.description


async def test_create_answer(client: AsyncClient, superuser_token_headers: dict[str: str], new_question: Question):
    new_answer = AnswerCreate(
        question_id=new_question.id,
        answer_text=await random_lower_string(),
        is_correct=True
    )
    response = await client.post("/answer", headers=await superuser_token_headers, json=new_answer.dict())
    assert response.status_code == 201


async def test_get_answers(db: Session, client: AsyncClient, superuser_token_headers: dict[str: str], new_question: Question):
    await create_random_answer(db, new_question.id)
    await create_random_answer(db, new_question.id)
    await create_random_answer(db, new_question.id)
    response = await client.get("/answers", headers=await superuser_token_headers)
    assert response.status_code == 200
    assert len(response.json()) > 1


async def test_get_answer(client: AsyncClient, superuser_token_headers: dict[str: str], new_correct_answer: Answer):
    response = await client.get(f"/answer/{new_correct_answer.id}", headers=await superuser_token_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_correct_answer.id
    assert response_data["question_id"] == new_correct_answer.question_id
    assert response_data["answer_text"] == new_correct_answer.answer_text
    assert response_data["is_correct"] == new_correct_answer.is_correct


async def test_update_answer(client: AsyncClient, superuser_token_headers: dict[str: str], new_correct_answer: Answer):
    update_answer = AnswerScheme(
        id=new_correct_answer.id,
        question_id=new_correct_answer.question_id,
        answer_text=await random_lower_string(),
        is_correct=False
    )
    response = await client.patch(
        f"/answer/{new_correct_answer.id}",
        headers=await superuser_token_headers,
        json=update_answer.dict()
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_correct_answer.id
    assert response_data["question_id"] == update_answer.question_id
    assert response_data["answer_text"] == update_answer.answer_text
    assert response_data["is_correct"] == update_answer.is_correct


async def test_delete_answer(client: AsyncClient, superuser_token_headers: dict[str: str], new_correct_answer: Answer):
    response = await client.delete(f"/answer/{new_correct_answer.id}", headers=await superuser_token_headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == new_correct_answer.id
    assert response_data["question_id"] == new_correct_answer.question_id
    assert response_data["answer_text"] == new_correct_answer.answer_text


async def test_get_results(db: Session, client: AsyncClient, superuser_token_headers: dict[str: str], new_normal_user: User, new_active_quiz: Quiz):
    await create_quiz_result(db, new_normal_user.id, new_active_quiz.id)
    await create_quiz_result(db, new_normal_user.id, new_active_quiz.id)
    await create_quiz_result(db, new_normal_user.id, new_active_quiz.id)
    response = await client.get("/results", headers=await superuser_token_headers)
    assert response.status_code == 200
    assert len(response.json()) > 1


async def test_get_result(client: AsyncClient, superuser_token_headers: dict[str: str], new_quiz_result: QuizResult):
    response = await client.get(f"/result/{new_quiz_result.id}", headers=await superuser_token_headers)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == new_quiz_result.id
    assert response_data["user_id"] == new_quiz_result.user_id
    assert response_data["quiz_id"] == new_quiz_result.quiz_id
    assert response_data["user_score"] == new_quiz_result.user_score
    assert response_data["max_score"] == new_quiz_result.max_score
    assert datetime.fromisoformat(response_data["finished_at"]) == new_quiz_result.finished_at


async def test_delete_result(client: AsyncClient, superuser_token_headers: dict[str: str], new_quiz_result: QuizResult):
    response = await client.delete(f"/result/{new_quiz_result.id}", headers=await superuser_token_headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == new_quiz_result.id
    assert response_data["user_id"] == new_quiz_result.user_id
    assert response_data["quiz_id"] == new_quiz_result.quiz_id
    assert response_data["user_score"] == new_quiz_result.user_score
    assert response_data["max_score"] == new_quiz_result.max_score
    assert datetime.fromisoformat(response_data["finished_at"]) == new_quiz_result.finished_at

