from dbms.db import db
from datetime import datetime

class Assignment(db.Model):
    __tablename__ = "assignments"
    id=db.Column(db.Integer,primary_key=True)
    institution_id=db.Column(db.Integer,db.ForeignKey("institutions.id"),nullable=False)
    course_id=db.Column(db.Integer,db.ForeignKey("courses.id"),nullable=False)
    batch_id=db.Column(db.Integer,db.ForeignKey("batches.id"),nullable=False)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.Text,nullable=True)
    due_date=db.Column(db.Date,nullable=True)
    max_marks=db.Column(db.Integer,nullable=True)
    status = db.Column(db.String(50), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    submissions = db.relationship(
    "AssignmentSubmission",
    backref="assignment",
    lazy=True,
    cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "course_id": self.course_id,
            "batch_id": self.batch_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "max_marks": self.max_marks,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }