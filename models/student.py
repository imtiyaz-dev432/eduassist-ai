from dbms.db import db
from datetime import datetime

class Student(db.Model):
    __tablename__='students'
    id=db.Column(db.Integer,primary_key=True)
    institution_id=db.Column(db.Integer,db.ForeignKey('institutions.id'),nullable=False)
    course_id=db.Column(db.Integer,db.ForeignKey('courses.id'),nullable=False)
    batch_id=db.Column(db.Integer,db.ForeignKey("batches.id"),nullable=False)
    student_name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(153),nullable=True)
    phone=db.Column(db.String(20),nullable=False)
    parent_phone=db.Column(db.String(20),nullable=True)
    address=db.Column(db.Text,nullable=True)
    admission_date=db.Column(db.Date,nullable=True)
    status = db.Column(db.String(50), default="Active")    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(255), nullable=True)
    is_login_enabled = db.Column(db.Boolean, default=False)
    fees = db.relationship("Fee", backref="student", lazy=True, cascade="all, delete-orphan")
    
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    payments = db.relationship(
    "Payment",
    backref="student",
    lazy=True,
    cascade="all, delete-orphan")
    attendance_records = db.relationship(
    "Attendance",
    backref="student",
    lazy=True,
    cascade="all, delete-orphan")

    fee_reminders = db.relationship(
    "FeeReminder",
    backref="student",
    lazy=True,
    cascade="all, delete-orphan")
    
    assignment_submissions = db.relationship(
    "AssignmentSubmission",
    backref="student",
    lazy=True,
    cascade="all, delete-orphan")

    quiz_submissions = db.relationship(
    "QuizSubmission",
    backref="student",
    lazy=True,
    cascade="all, delete-orphan")

    def to_dict(self):
       return {
        "id": self.id,
        "institution_id": self.institution_id,
        "course_id": self.course_id,
        "batch_id": self.batch_id,
        "student_name": self.student_name,
        "email": self.email,
        "phone": self.phone,
        "parent_phone": self.parent_phone,
        "address": self.address,
        "admission_date": self.admission_date.isoformat() if self.admission_date else None,
        "status": self.status,
        "is_login_enabled": self.is_login_enabled,
        "created_at": self.created_at.isoformat() if self.created_at else None,
        "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }

  