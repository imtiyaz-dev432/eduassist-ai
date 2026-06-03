from dbms.db import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__="attendances"
    id=db.Column(db.Integer,primary_key=True)
    institution_id=db.Column(db.Integer,db.ForeignKey("institutions.id"),nullable=False)
    batch_id=db.Column(db.Integer,db.ForeignKey("batches.id"),nullable=False)
    course_id=db.Column(db.Integer,db.ForeignKey("courses.id"),nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)
    attendance_date=db.Column(db.Date,nullable=False)
    status=db.Column(db.String(50),nullable=False)
    remarks=db.Column(db.Text,nullable=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "course_id": self.course_id,
            "batch_id": self.batch_id,
            "student_id": self.student_id,
            "attendance_date": self.attendance_date.isoformat() if self.attendance_date else None,
            "status": self.status,
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }