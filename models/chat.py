from dbms.db import db
from datetime import datetime

class ChatHistory(db.Model):
    __tablename__="chat_history"
    id=db.Column(db.Integer,primary_key=True)
    institution_id = db.Column(
        db.Integer,
        db.ForeignKey("institutions.id"),
        nullable=False
    )
    lead_id = db.Column(
        db.Integer,
        db.ForeignKey("leads.id"),
        nullable=True
    )
    sender = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "lead_id": self.lead_id,
            "sender": self.sender,
            "message": self.message,
            "response": self.response,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }