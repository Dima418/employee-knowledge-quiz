"""Utility functions for quiz data

"""

from app.database.models.quiz import Quiz, Answer
from app.schemes.quiz import (
    QuizResponse,
    QuestionResponse,
    QuestionRequset,
    QuestionAnswerVariantResponse,
    UserAnswerRequset
)


async def generate_quiz_response(quiz: Quiz) -> QuizResponse:
    """Generate quiz response for user to answer.

    Args:
        quiz (Quiz): The quiz.

    Returns:
        (QuizResponse): Quiz with questions and answers.
    """
    questions_response: list[QuestionResponse] = []

    for question in quiz.questions:
        answer_variants: list[QuestionAnswerVariantResponse] = []
        for answer in question.answers:
            answer_variants.append(
                QuestionAnswerVariantResponse(
                    answer_id=answer.id,
                    answer_text=answer.answer_text
                )
            )

        questions_response.append(
            QuestionResponse(
                question_id=question.id,
                question_text=question.question_text,
                answer_variants=answer_variants
            )
        )

    quiz_response = QuizResponse(
        quiz_id=quiz.id,
        quiz_title=quiz.title,
        quiz_description=quiz.description,
        questions=questions_response,
    )
    return quiz_response


async def get_quiz_max_score(quiz: Quiz) -> int | None:
    """Get max score for the quiz.

    Args:
        quiz (Quiz): The quiz.

    Returns:
        (int, optional): The max score.
    """
    max_score: int = 0
    for question in quiz.questions:
        for answer in question.answers:
            if answer.is_correct:
                max_score += 1
    return max_score if max_score > 0 else None


async def get_question_ids(quiz: Quiz) -> list[int] | None:
    """Get question ids for the quiz.

    Args:
        quiz (Quiz): The quiz.

    Returns:
        (list[int], optional): List of question ids.
    """
    questions_ids: list[int] = [question.id for question in quiz.questions]
    return questions_ids if questions_ids else None


async def get_answers_ids(quiz: Quiz) -> list[int] | None:
    """Get answer ids for the quiz.

    Args:
        quiz (Quiz): The quiz.

    Returns:
        (list[int], optional): List of answer ids.
    """
    answers_ids: list[int] = []
    for question in quiz.questions:
        for answer in question.answers:
            answers_ids.append(answer.id)

    return answers_ids if answers_ids else None


async def get_answers(quiz: Quiz) -> list[Answer]:
    """Get all answers for quiz.

    Args:
        quiz (Quiz): The quiz.

    Returns:
        (list[Answer]): The list of answers.
    """
    answers: list[Answer] = []
    for question in quiz.questions:
        for answer in question.answers:
            answers.append(answer)

    return answers


async def select_user_answers(questions: list[QuestionRequset]) -> list[UserAnswerRequset] | None:
    """Select user answers from the quiz request.

    Args:
        questions (list[QuestionRequset]): The list of questions.

    Returns:
        (list[UserAnswerRequset], optional): List of user answers.
    """
    user_answers: list[UserAnswerRequset] = []
    for question in questions:
        for user_answer in question.user_answers:
            user_answers.append(user_answer)

    return user_answers if user_answers else None