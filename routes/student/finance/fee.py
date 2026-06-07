from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from models.student import Student
from models.fee import Fee

student_fee_bp=Blueprint(
    "student_fee_bp",__name__,
    url_prefix="/student/finance/fee"
)
@student_fee_bp.route("/my",methods=["GET"])
@jwt_required()
def my_fee():
    claims=get_jwt()
    if claims.get("role")!="student":
        return jsonify({
             "success": False,
            "message": "Student access only"
        }),403

    current_student_id=int(get_jwt_identity())
    student=Student.query.filter_by(
        id=current_student_id
    ).first()

    if not student:
        return jsonify({
            "success":False,
            "message":"Student not found"
        }),400
    fees=Fee.query.filter_by(
        student_id=student.id
    ).all()

    fee_list=[]
    for fee in fees:
        fee_list.append(fee.to_dict())

    return jsonify({
        "success": True,
        "message": "Fees fetched successfully",
        "fees": fee_list
    }), 200    