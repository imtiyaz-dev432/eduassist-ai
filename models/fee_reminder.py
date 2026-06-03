from dbms.db import db
from datetime import datetime

class FeeReminder(db.Model):
    __tablename__="fee_reminders"
    id=db.Column(db.Integer,primary_key=True)
    institution_id=db.Column(db.Integer,db.ForeignKey("institutions.id"),nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey("students.id"),nullable=False)
    fee_id=db.Column(db.Integer,db.ForeignKey("fees.id"),nullable=False)
    reminder_date=db.Column(db.Date,nullable=False)
    message=db.Column(db.Text,nullable=True)
    status=db.Column(db.String(50),default='Pending')
    sent_at=db.Column(db.DateTime,nullable=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "student_id": self.student_id,
            "fee_id": self.fee_id,
            "reminder_date": self.reminder_date.isoformat() if self.reminder_date else None,
            "message": self.message,
            "status": self.status,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
