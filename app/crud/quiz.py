from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.database.models.quiz import (
    Answer,
    Quiz,
    Category,
    Question,
    QuizResult
)
from app.schemes.quiz import (
    QuizCreate,
    QuestionCreate,
    CategoryCreate,
    AnswerCreate
)


class CRUDAnswer(CRUDBase):
    async def get_answers(self, db: Session, quiz_id: int) -> list:
        answers = db.query(Answer)\
        .join(Answer.question)\
        .join(Question.quiz)\
        .filter(Quiz.id == quiz_id)\
        .all()
        return answers

    async def get_correct_answers(self, db: Session, question_id: int) -> bool:
        correct_answers = db.query(Answer.id, Answer.is_correct)\
        .join(Answer.question)\
        .filter(Question.id == question_id)\
        .filter(Answer.is_correct == True)\
        .all()
        return correct_answers

    async def exists(self, db: Session, answer: AnswerCreate) -> bool:
        _answer = db.query(Answer)\
            .filter(Answer.answer_text == answer.answer_text)\
            .join(Answer.question)\
            .filter(Question.id == answer.question_id)\
            .filter(Answer.question_id == answer.question_id)\
            .first()
        return _answer is not None


class CRUDQuiz(CRUDBase):
    async def exists(self, db: Session, quiz: QuizCreate) -> bool:
        _quiz = db.query(Quiz)\
            .filter(
                Quiz.title == quiz.title,
                Quiz.description == quiz.description
            ).first()
        return _quiz is not None


class CRUDQuestion(CRUDBase):
    async def exists(self, db: Session, question: QuestionCreate) -> bool:
        _question = db.query(Question)\
            .join(Question.quiz)\
            .filter(Quiz.id == question.quiz_id)\
            .filter(Question.question_text == question.question_text)\
            .first()
        return _question is not None


class CRUDCategory(CRUDBase):
    async def exists(self, db: Session, category: CategoryCreate) -> bool:
        _category = db.query(Category)\
            .filter(Category.name == category.name)\
            .first()
        return _category is not None


class CRUDQuizResult(CRUDBase):
    pass


crud_answer = CRUDAnswer(Answer)
crud_quiz = CRUDQuiz(Quiz)
crud_question = CRUDQuestion(Question)
crud_category = CRUDCategory(Category)
crud_quiz_result = CRUDQuizResult(QuizResult)
