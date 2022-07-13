"""Quiz routes.

"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.quiz import crud_quiz
from app.database.models.quiz import Answer, Quiz
from app.database.models.user import User
from app.database.session import get_db
from app.schemes.quiz import (
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

@router.get("/quiz/{quiz_id}/start", response_model=QuizResponse)
async def all_quizzes(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve quiz with specific id.

    Args:
        quiz_id (int): Quiz id.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): Current authenticated user. Defaults to Depends(get_current_user).

    Raises:
        HTTP_404_NOT_FOUND (HTTPException): Raised if quiz is not found.

    Returns:
        quiz_response (QuizResponse): Quiz with questions and answers.
    """
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
    """Submit quiz.

    Args:
        quiz_id (int): Quiz id.
        quiz_request (QuizRequset): Quiz request with answers.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): Current authenticated user. Defaults to Depends(get_current_user).

    Raises:
        HTTP_400_BAD_REQUEST (HTTPException): Quiz id mismatch.
            ``quiz_id`` does not match ``quiz_request.quiz_id``.
        HTTP_400_BAD_REQUEST (HTTPException): Quiz has no questions or answers.
            Quiz is empty.
        HTTP_400_BAD_REQUEST (HTTPException): Quiz don't have any questions.
            Quiz has no correct questions.
        HTTP_400_BAD_REQUEST (HTTPException): Incorrect number of answers provided.
            Answers provided by user does not match number of answers in questions.
        HTTP_400_BAD_REQUEST (HTTPException): Incorrect answer id provided. Quiz has no correct questions.
            Answer provided by user does not match any of answers in questions
        HTTP_404_NOT_FOUND (HTTPException): Quiz not found.
            No quiz found with id ``quiz_id``.

    Returns:
        (dict):
            max_score (int): Max score for quiz.
            user_score (int): User score for quiz.
    """
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
        raise HTTP_400_BAD_REQUEST("Quiz don't have any correct questions")

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
