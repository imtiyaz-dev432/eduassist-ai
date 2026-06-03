from dbms.db import db
from datetime import datetime

class Faq(db.Model):
    __tablename__="faqs"
    id=db.Column(db.Integer,primary_key=True)
    institution_id=db.Column(db.Integer,db.ForeignKey("institutions.id"),nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True)  
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 