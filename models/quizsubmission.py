from dbms.db import db
from datetime import datetime


class QuizSubmission(db.Model):
    __tablename__ = "quiz_submissions"

    id = db.Column(db.Integer, primary_key=True)

    institution_id = db.Column(
        db.Integer,
        db.ForeignKey("institutions.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey("batches.id"),
        nullable=False
    )

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quizzes.id"),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    total_marks = db.Column(db.Float, nullable=True)
    obtained_marks = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default="Submitted")
    teacher_feedback = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    checked_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    answers = db.relationship(
        "QuizSubmissionAnswer",
        backref="quiz_submission",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "course_id": self.course_id,
            "batch_id": self.batch_id,
            "quiz_id": self.quiz_id,
            "student_id": self.student_id,
            "total_marks": self.total_marks,
            "obtained_marks": self.obtained_marks,
            "status": self.status,
            "teacher_feedback": self.teacher_feedback,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "checked_at": self.checked_at.isoformat() if self.checked_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }