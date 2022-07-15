from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.quiz import (
    crud_answer,
    crud_quiz,
    crud_question,
    crud_category,
    crud_quiz_result
)
from app.database.models.user import User
from app.database.models.quiz import (
    Answer,
    Quiz,
    QuizResult
)
from app.database.session import get_db
from app.schemes.quiz import (
    CategoryCreate,
    CategoryScheme,
    AnswerCreate,
    AnswerScheme,
    QuestionCreate,
    QuestionScheme,
    QuizCreate,
    QuizScheme,
    QuizRequset,
    QuizResponse,
    QuizResultResponse,
    QuizResultScheme
)
from app.utils.quiz import (
    generate_quiz_response,
    get_quiz_max_score,
    get_question_ids,
    get_answers_ids,
    get_real_answers
)
from app.utils.user import get_current_user, get_current_superuser
from app.utils.HTTP_errors import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


router = APIRouter(tags=["quiz"])

@router.get("/quiz/{quiz_id}/view", response_model=QuizResponse)
async def all_quizzes(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz: Quiz = await crud_quiz.get(id=quiz_id, db=db)
    if not quiz:
        raise HTTP_404_NOT_FOUND("Quiz not found")
    return await generate_quiz_response(quiz)


@router.post("/quiz/{quiz_id}/submit", response_model=QuizResultResponse)
async def submit_quiz(
    quiz_id: int,
    quiz_request: QuizRequset,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if quiz_id != quiz_request.quiz_id:
        raise HTTP_400_BAD_REQUEST("Quiz id mismatch")

    quiz: Quiz = await crud_quiz.get(id=quiz_id, db=db)

    if not quiz:
        raise HTTP_404_NOT_FOUND("Quiz not found")

    if not quiz.is_active:
        raise HTTP_404_NOT_FOUND("Quiz is not active")

    questions_ids: list[int] = await get_question_ids(quiz)
    quiz_answers_ids: list[int] = await get_answers_ids(quiz)
    quiz_answers: list[Answer] = await get_real_answers(quiz)

    if not questions_ids or not quiz_answers_ids:
        raise HTTP_400_BAD_REQUEST("Quiz has no questions or answers")

    max_score = await get_quiz_max_score(quiz)

    if not max_score:
        raise HTTP_400_BAD_REQUEST("Quiz don't have any correct questions")

    user_answers = quiz_request.answers

    if not user_answers or len(user_answers) != len(quiz_answers_ids):
        raise HTTP_400_BAD_REQUEST("Incorrect number of answers provided")

    for user_answer in user_answers:
        if user_answer.answer_id not in quiz_answers_ids:
            raise HTTP_400_BAD_REQUEST("Incorrect answer id provided")

    user_score: int = max_score

    for user_answer in user_answers:
        for quiz_answer in quiz_answers:
            if user_answer.answer_id == quiz_answer.id:
                if quiz_answer.is_correct != user_answer.is_correct:
                    user_score -= 1

    await crud_quiz_result.create(
        db=db,
        new_obj=QuizResult(
            user_id=current_user.id,
            quiz_id=quiz_id,
            max_score=max_score,
            user_score=user_score
        )
    )
    return QuizResultResponse(max_score=max_score, user_score=user_score)


@router.post("/quiz", response_model=QuizScheme, status_code=201)
async def create_quiz(
    quiz: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> QuizScheme:
    if await crud_quiz.exists(db, quiz):
        raise HTTP_400_BAD_REQUEST("Quiz already exists")
    return await crud_quiz.create(db, new_obj=quiz)


@router.get("/quizzes", response_model=list[QuizScheme])
async def get_quizzes(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> list[QuizScheme]:
    quizzes = await crud_quiz.get_multi(db, skip=skip, limit=limit)
    if not quizzes:
        raise HTTP_404_NOT_FOUND("Quizzes not found")
    return quizzes


@router.get("/quiz/{quiz_id}", response_model=QuizScheme)
async def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> QuizScheme:
    quiz = await crud_quiz.get(db, id=quiz_id)
    if not quiz:
        raise HTTP_404_NOT_FOUND("Quiz not found")
    return quiz


@router.patch("/quiz/{quiz_id}")
async def update_quiz(
    quiz_id: int,
    quiz_in: QuizScheme,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    if quiz_id != quiz_in.id:
        raise HTTP_400_BAD_REQUEST("Quiz id mismatch")

    quiz = await crud_quiz.get(db, id=quiz_id)
    if not quiz:
        raise HTTP_404_NOT_FOUND("Quiz not found")

    return await crud_quiz.update(db, old_obj=quiz, new_obj=quiz_in)


@router.delete("/quiz/{quiz_id}")
async def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    quiz = await crud_quiz.get(db, id=quiz_id)
    if not quiz:
        raise HTTP_404_NOT_FOUND("Quiz not found")
    return await crud_quiz.delete(db, id=quiz_id)


@router.post("/question", response_model=QuestionScheme, status_code=201)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> QuestionScheme:
    if await crud_question.exists(db, question):
        raise HTTP_400_BAD_REQUEST("Question already exists")

    if not await crud_quiz.get(db, id=question.quiz_id):
        raise HTTP_404_NOT_FOUND("Quiz not found")

    return await crud_question.create(db, new_obj=question)


@router.get("/questions", response_model=list[QuestionScheme])
async def get_questions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> list[QuestionScheme]:
    questions = await crud_question.get_multi(db, skip=skip, limit=limit)
    if not questions:
        return HTTP_404_NOT_FOUND("Questions not found")
    return questions


@router.get("/question/{question_id}", response_model=QuestionScheme)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> QuestionScheme:
    question = await crud_question.get(db, id=question_id)
    if not question:
        raise HTTP_404_NOT_FOUND("Question not found")
    return question


@router.patch("/question/{question_id}")
async def update_question(
    question_id: int,
    question_in: QuestionScheme,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    if question_id != question_in.id:
        raise HTTP_400_BAD_REQUEST("Question id mismatch")

    if not await crud_quiz.get(db, id=question_in.quiz_id):
        raise HTTP_404_NOT_FOUND("Quiz not found")

    question = await crud_question.get(db, id=question_id)
    if not question:
        raise HTTP_404_NOT_FOUND("Question not found")

    return await crud_question.update(db, old_obj=question, new_obj=question_in)


@router.delete("/question/{question_id}")
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    question = await crud_question.get(db, id=question_id)
    if not question:
        raise HTTP_404_NOT_FOUND("Question not found")
    return await crud_question.delete(db, id=question_id)


@router.post("/category", response_model=CategoryScheme, status_code=201)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> CategoryScheme:
    if await crud_category.exists(db, category):
        raise HTTP_400_BAD_REQUEST("Category already exists")
    return await crud_category.create(db, new_obj=category)


@router.get("/categories", response_model=list[CategoryScheme])
async def get_categories(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> list[CategoryScheme]:
    categories = await crud_category.get_multi(db, skip=skip, limit=limit)
    if not categories:
        raise HTTP_404_NOT_FOUND("Categories not found")
    return categories


@router.get("/category/{category_id}", response_model=CategoryScheme)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> CategoryScheme:
    category = await crud_category.get(db, id=category_id)
    if not category:
        return HTTP_404_NOT_FOUND("Category not found")
    return category


@router.patch("/category/{category_id}")
async def update_category(
    category_id: int,
    category_in: CategoryScheme,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    if category_id != category_in.id:
        raise HTTP_400_BAD_REQUEST("Category id mismatch")

    category = await crud_category.get(db, id=category_id)
    if not category:
        raise HTTP_404_NOT_FOUND("Category not found")

    return await crud_category.update(db, old_obj=category, new_obj=category_in)


@router.delete("/category/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    category = await crud_category.get(db, id=category_id)
    if not category:
        raise HTTP_404_NOT_FOUND("Category not found")
    return await crud_category.delete(db, id=category_id)


@router.post("/answer", response_model=AnswerScheme, status_code=201)
async def create_answer(
    answer: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> AnswerScheme:
    if await crud_answer.exists(db, answer):
        raise HTTP_400_BAD_REQUEST("Answer already exists")

    if not await crud_question.get(db, id=answer.question_id):
        raise HTTP_404_NOT_FOUND("Question not found")

    return await crud_answer.create(db, new_obj=answer)


@router.get("/answers", response_model=list[AnswerScheme])
async def get_answers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> list[AnswerScheme]:
    answers = await crud_answer.get_multi(db, skip=skip, limit=limit)
    if not answers:
        raise HTTP_404_NOT_FOUND("Answers not found")
    return answers


@router.get("/answer/{answer_id}", response_model=AnswerScheme)
async def get_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> AnswerScheme:
    answer = await crud_answer.get(db, id=answer_id)
    if not answer:
        raise HTTP_404_NOT_FOUND("Answer not found")
    return answer


@router.patch("/answer/{answer_id}")
async def update_answer(
    answer_id: int,
    answer_in: AnswerScheme,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
):
    if answer_id != answer_in.id:
        raise HTTP_400_BAD_REQUEST("Answer id mismatch")

    if not await crud_question.get(db, id=answer_in.question_id):
        raise HTTP_404_NOT_FOUND("Question not found")

    answer = await crud_answer.get(db, id=answer_id)
    if not answer:
        raise HTTP_404_NOT_FOUND("Answer not found")

    return await crud_answer.update(db, old_obj=answer, new_obj=answer_in)


@router.delete("/answer/{answer_id}")
async def delete_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    answer = await crud_answer.get(db, id=answer_id)
    if not answer:
        raise HTTP_404_NOT_FOUND("Answer not found")
    return await crud_answer.delete(db, id=answer_id)


@router.get("/results", response_model=list[QuizResultScheme])
async def get_answers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> list[QuizResultScheme]:
    results = await crud_quiz_result.get_multi(db, skip=skip, limit=limit)
    if not results:
        raise HTTP_404_NOT_FOUND("Results not found")
    return results


@router.get("/result/{result_id}", response_model=QuizResultScheme)
async def get_answer(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> QuizResultScheme:
    result = await crud_quiz_result.get(db, id=result_id)
    if not result:
        raise HTTP_404_NOT_FOUND("Result not found")
    return result


@router.delete("/result/{result_id}")
async def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    result = await crud_quiz_result.get(db, id=result_id)
    if not result:
        raise HTTP_404_NOT_FOUND("Result not found")
    return await crud_quiz_result.delete(db, id=result_id)
