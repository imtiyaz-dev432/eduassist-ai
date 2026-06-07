from dbms.db import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    institution_id = db.Column(
        db.Integer,
        db.ForeignKey("institutions.id"),
        nullable=False
    )
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    fee_id = db.Column(
        db.Integer,
        db.ForeignKey("fees.id"),
        nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  
    transaction_id = db.Column(db.String(150), nullable=True)
    payment_status = db.Column(db.String(50), default="Success")
    receipt_no = db.Column(db.String(100), nullable=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "institution_id": self.institution_id,
            "student_id": self.student_id,
            "fee_id": self.fee_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "transaction_id": self.transaction_id,
            "payment_status": self.payment_status,
            "receipt_no": self.receipt_no,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }