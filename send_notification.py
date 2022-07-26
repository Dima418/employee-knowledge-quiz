from datetime import datetime, timedelta

from app.database import base
from app.database.session import SessionLocal
from app.database.models.quiz import Quiz, QuizResult
from app.database.models.user import User
from app.utils.send_email import send_email


with SessionLocal() as db:
    for expired_quiz_result in db.query(Quiz.id, Quiz.title, QuizResult.finished_at, User.name, User.email)\
        .join(User.quiz_results)\
        .join(QuizResult.quiz)\
        .filter(QuizResult.finished_at <= datetime.utcnow() - timedelta(days=7))\
        .order_by(Quiz.id, Quiz.title, QuizResult.finished_at, User.name, User.email):
        result_obj = expired_quiz_result._asdict()
        send_email(
            to_email=result_obj['email'],
            subject=f"Quiz \"{result_obj['title']}\" expired",
            content=f"Dear {result_obj['name']}, Quiz \"{result_obj['title']}\" is expired. Please, finish it as soon as possible."
        )
