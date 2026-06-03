from dbms.db import db
from datetime import datetime


class QuizSubmissionAnswer(db.Model):
    __tablename__ = "quiz_submission_answers"

    id = db.Column(db.Integer, primary_key=True)
    quiz_submission_id = db.Column(
        db.Integer,
        db.ForeignKey("quiz_submissions.id"),
        nullable=False
    )
    quiz_question_id = db.Column(
        db.Integer,
        db.ForeignKey("quiz_questions.id"),
        nullable=False
    )
    student_answer = db.Column(db.String(500), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)
    marks_awarded = db.Column(db.Float, nullable=True)
    teacher_feedback = db.Column(db.Text, nullable=True)
    checked_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "quiz_submission_id": self.quiz_submission_id,
            "quiz_question_id": self.quiz_question_id,
            "student_answer": self.student_answer,
            "is_correct": self.is_correct,
            "marks_awarded": self.marks_awarded,
            "teacher_feedback": self.teacher_feedback,
            "checked_at": self.checked_at.isoformat() if self.checked_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }