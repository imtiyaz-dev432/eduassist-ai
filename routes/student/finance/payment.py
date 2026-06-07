from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.student import Student
from models.payment import Payment

student_payment_bp=Blueprint("student_payment_bp",__name__,url_prefix="/student/finance/payment")
@student_payment_bp.route("/my",methods=["GET"])
@jwt_required()
def my_payment():
    claims=get_jwt()
    if claims.get("role")!="student":
        return jsonify({
            "success":False,
            "message":"Student access only"
        }),403
    current_student_id=int(get_jwt_identity())    
    student=Student.query.filter_by(
        id=current_student_id
    ).first()

    if not student:
        return jsonify({
            "success":False,
            "message":"Student not found"
        }),404
    payments=Payment.query.filter_by(
        student_id=student.id
    ).all()

    payment_list=[]
    for payment in payments:
        payment_list.append(payment.to_dict())

    return jsonify({
        "success": True,
        "message": "Payments fetched successfully",
        "payments": payment_list
    }),200