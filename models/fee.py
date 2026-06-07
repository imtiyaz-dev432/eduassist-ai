from dbms.db import db
from datetime import datetime

class Fee(db.Model):
    __tablename__="fees"
    id=db.Column(db.Integer,primary_key=True)
    institution_id=db.Column(db.Integer,db.ForeignKey("institutions.id"),nullable=False)
    course_id=db.Column(db.Integer,db.ForeignKey("courses.id"),nullable=False)
    batch_id=db.Column(db.Integer,db.ForeignKey("batches.id"),nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)
    total_fee=db.Column(db.Float,nullable=False)
    paid_amount = db.Column(db.Float, default=0)
    due_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default="Pending")   
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    payments = db.relationship(
    "Payment",
    backref="fee",
    lazy=True,
    cascade="all, delete-orphan"
)
    fee_reminders = db.relationship(
    "FeeReminder",
    backref="fee",
    lazy=True,
    cascade="all, delete-orphan"
)
    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "course_id": self.course_id,
            "batch_id": self.batch_id,
            "student_id": self.student_id,
            "total_fee": self.total_fee,
            "paid_amount": self.paid_amount,
            "due_amount": self.due_amount,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
