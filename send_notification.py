from datetime import datetime, timedelta
from sqlalchemy.sql.expression import func

from app.database import base
from app.database.session import SessionLocal
from app.database.models.quiz import Quiz, QuizResult
from app.database.models.user import User
from app.utils.send_email import send_email


with SessionLocal() as db:
    quiz_results = db.query(
            QuizResult.quiz_id,
            QuizResult.user_id,
            func.max(QuizResult.finished_at).label("finished_at")
        ).group_by(QuizResult.quiz_id, QuizResult.user_id).cte("quiz_results")
    for expired_quiz_result in db.query(Quiz.id, Quiz.title, quiz_results.c.finished_at, User.name, User.email)\
        .join(User, quiz_results.c.user_id == User.id)\
        .join(Quiz, quiz_results.c.quiz_id == Quiz.id)\
        .filter(quiz_results.c.finished_at <= datetime.utcnow() - timedelta(days=7))\
        .order_by(Quiz.id, Quiz.title, quiz_results.c.finished_at, User.name, User.email):
        result_obj = expired_quiz_result._asdict()
        send_email(
            to_email=result_obj['email'],
            subject=f"Quiz \"{result_obj['title']}\" expired",
            content=f"Dear {result_obj['name']}, Quiz \"{result_obj['title']}\" is expired. Please, finish it as soon as possible."
        )
