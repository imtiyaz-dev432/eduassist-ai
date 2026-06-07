from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from models.student import Student
student_auth_bp=Blueprint("student_auth_bp",__name__,url_prefix="/student_auth")
@student_auth_bp.route("/login",methods=["POST"])
def login_student():
    data=request.get_json()
    if not data:
        return jsonify({
            "success":False,
            "message":"Request body is required"
        }),400
    identifier=data.get("identifier")
    password=data.get("password")
    if not identifier or not password:
        return jsonify({
            "success":False,
            "message":"Email/Mobile and password is required"
        }),400
    identifier = identifier.strip().lower()
    student=Student.query.filter(
        (Student.phone==identifier) | (Student.email==identifier)
    ).first()

    if not student:
     return jsonify({
        "success":False,
        "message":"Invalid phone/email or password"
    }),401
    
    if not student.is_login_enabled:
        return jsonify({
            "success": False,
            "message": "Student login is not enabled. Please contact your institute."
        }), 403

    if not student.password_hash:
        return jsonify({ "success": False,
            "message": "Student password is not set. Please contact your institute."
        }), 403
    if not check_password_hash(student.password_hash, password):
        return jsonify({
            "success": False,
            "message": "Invalid phone/email or password"
        }), 401

    access_token = create_access_token(
        identity=str(student.id),
        additional_claims={
            "role": "student"
        }
    )

    return jsonify({
        "success": True,
        "message": "Student login successful",
        "access_token": access_token,
        "student": student.to_dict()
    }), 200        

#