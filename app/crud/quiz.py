from sqlalchemy.orm import Session, load_only

from app.crud.base import CRUDBase
from app.database.base import Quiz, Question, Answer


class CRUDQuiz(CRUDBase):
    async def get_answers(self, db: Session, quiz_id: int) -> list:
        answers = db.query(Answer)\
        .join(Answer.question)\
        .join(Question.quiz)\
        .filter(Quiz.id == quiz_id)\
        .all()
        return answers


class CRUDQuestion(CRUDBase):
    async def get_correct_answers(self, db: Session, question_id: int) -> bool:
        correct_answers = db.query(Answer.id, Answer.is_correct)\
        .join(Answer.question)\
        .filter(Question.id == question_id)\
        .filter(Answer.is_correct == True)\
        .all()
        return correct_answers


class CRUDAnswer(CRUDBase):
    pass


crud_quiz = CRUDQuiz(Quiz)
crud_question = CRUDQuestion(Question)
crud_answer = CRUDAnswer(Answer)
