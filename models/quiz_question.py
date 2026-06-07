from dbms.db import db
from datetime import datetime


class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quizzes.id"),
        nullable=False
    )
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(10), nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    marks = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    submission_answers = db.relationship(
    "QuizSubmissionAnswer",
    backref="quiz_question",
    lazy=True,
    cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "question": self.question,
            "option_a": self.option_a,
            "option_b": self.option_b,
            "option_c": self.option_c,
            "option_d": self.option_d,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "marks": self.marks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    def to_dict_for_student(self):
     return {
        "id": self.id,
        "quiz_id": self.quiz_id,
        "question": self.question,
        "option_a": self.option_a,
        "option_b": self.option_b,
        "option_c": self.option_c,
        "option_d": self.option_d,
        "marks": self.marks
    }

    