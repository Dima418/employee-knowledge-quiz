"""CRUD classes for quiz models.

"""

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.database.models.quiz import Quiz, Question, Answer


class CRUDQuiz(CRUDBase):
    """Class for CRUD operations on ``Quiz`` model.

    Args:
        CRUDBase: The CRUD base class.
    """

    async def get_answers(self, db: Session, quiz_id: int) -> list:
        """Get all answers for quiz.

        Args:
            db (Session): The database session.
            quiz_id (int): The quiz id.

        Returns:
            (list): The list of answers.
        """
        answers = db.query(Answer)\
        .join(Answer.question)\
        .join(Question.quiz)\
        .filter(Quiz.id == quiz_id)\
        .all()
        return answers


class CRUDQuestion(CRUDBase):
    """Class for CRUD operations on ``Question`` model.

    Args:
        CRUDBase: The CRUD base class.
    """

    async def get_correct_answers(self, db: Session, question_id: int) -> bool:
        """Get all correct answers for question.

        Args:
            db (Session): The database session.
            question_id (int): The question id.

        Returns:
            (list[dict[str: Answer.id | Answer.is_correct]]): The list of correct answers.
        """
        correct_answers = db.query(Answer.id, Answer.is_correct)\
        .join(Answer.question)\
        .filter(Question.id == question_id)\
        .filter(Answer.is_correct == True)\
        .all()
        return correct_answers


class CRUDAnswer(CRUDBase):
    """Class for CRUD operations on ``Answer`` model.

    Args:
        CRUDBase: The CRUD base class.
    """
    pass


crud_quiz = CRUDQuiz(Quiz)
crud_question = CRUDQuestion(Question)
crud_answer = CRUDAnswer(Answer)
