from dbms.db import db
from datetime import datetime

class Course(db.Model):
    __tablename__='courses'
    id=db.Column(db.Integer,primary_key=True)
    institution_id=db.Column(db.Integer,db.ForeignKey('institutions.id'),nullable=False)
    course_name=db.Column(db.String(250),nullable=False)
    category=db.Column(db.String(50),nullable=True)
    course_fee=db.Column(db.Float,nullable=True)
    duration=db.Column(db.String(150),nullable=True)
    mode=db.Column(db.String(50),nullable=True)
    level=db.Column(db.String(50),nullable=True)
    description=db.Column(db.Text,nullable=True)
    syllabus = db.Column(db.Text, nullable=True)
    eligibility = db.Column(db.Text, nullable=True)
    certificate_available = db.Column(db.Boolean, default=False)
    placement_support = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    batches = db.relationship(
    "Batch",
    backref="course",
    lazy=True,
    cascade="all, delete-orphan")

    students = db.relationship(
    "Student",
    backref="course",
    lazy=True,
    cascade="all, delete-orphan")

    fee_records = db.relationship("Fee", backref="course", lazy=True, cascade="all, delete-orphan")
    attendance_records = db.relationship(
    "Attendance",
    backref="course",
    lazy=True,
    cascade="all, delete-orphan")

    assignments = db.relationship(
    "Assignment",
    backref="course",
    lazy=True,
    cascade="all, delete-orphan")

    assignment_submissions = db.relationship(
    "AssignmentSubmission",
    backref="course",
    lazy=True,
    cascade="all, delete-orphan")