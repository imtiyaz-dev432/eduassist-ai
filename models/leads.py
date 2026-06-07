from dbms.db import db
from datetime import datetime

class Lead(db.Model):
    __tablename__="leads"
    id=db.Column(db.Integer,primary_key=True)
    institution_id=db.Column(db.Integer,db.ForeignKey("institutions.id"),nullable=False)
    name=db.Column(db.String(120),nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(100),nullable=True)
    course_interest=db.Column(db.String(100),nullable=True)
    message=db.Column(db.Text,nullable=True)
    source=db.Column(db.String(50),default="Website")
    status=db.Column(db.String(50),default="New")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chat_history = db.relationship(
    "ChatHistory",
    backref="lead",
    lazy=True,
    cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "course_interest": self.course_interest,
            "message": self.message,
            "source": self.source,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }