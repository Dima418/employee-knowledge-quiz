from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.quiz import crud_quiz
from app.database.base import (
    Answer,
    Quiz,
    User
)
from app.database.session import get_db
from app.schemes import (
    QuizRequset,
    QuizResponse
)
from app.utils.quiz import (
    generate_quiz_response,
    get_quiz_max_score,
    get_question_ids,
    get_answers_ids,
    get_answers,
    select_user_answers
)
from app.utils.user import get_current_user
from app.utils.HTTP_errors import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


router = APIRouter(tags=["quiz"])

@router.get("/quiz/{quiz_id}/start")
async def all_quizzes(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz: Quiz = await crud_quiz.get(id=quiz_id, db=db)
    if quiz is None:
        raise HTTP_404_NOT_FOUND("Quiz not found")

    quiz_response: QuizResponse = await generate_quiz_response(quiz)
    return quiz_response


@router.post("/quiz/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: int,
    quiz_request: QuizRequset,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if quiz_id != quiz_request.quiz_id:
        raise HTTP_400_BAD_REQUEST("Quiz id mismatch")

    quiz: Quiz = await crud_quiz.get(id=quiz_id, db=db)

    if quiz is None:
        raise HTTP_404_NOT_FOUND("Quiz not found")

    questions_ids: list[int] = await get_question_ids(quiz)
    quiz_answers_ids: list[int] = await get_answers_ids(quiz)
    quiz_answers: list[Answer] = await get_answers(quiz)

    if not questions_ids or not quiz_answers_ids:
        raise HTTP_400_BAD_REQUEST("Quiz has no questions or answers")

    max_score = await get_quiz_max_score(quiz)

    if max_score is None:
        raise HTTP_400_BAD_REQUEST("Quiz don't have any questions")

    user_answers = await select_user_answers(quiz_request.questions)

    if not user_answers or len(user_answers) != len(quiz_answers_ids):
        raise HTTP_400_BAD_REQUEST("Incorrect number of answers provided")

    for user_answer in user_answers:
        if user_answer.answer_id not in quiz_answers_ids:
            raise HTTP_400_BAD_REQUEST("Incorrect answer id provided")

    user_score: int = 0

    for user_answer in user_answers:
        for quiz_answer in quiz_answers:
            if user_answer.answer_id == quiz_answer.id:
                if quiz_answer.is_correct and user_answer.is_correct:
                    user_score += 1


    return {"max_score": max_score, "user_score": user_score}
