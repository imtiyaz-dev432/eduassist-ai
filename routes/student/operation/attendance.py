from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.student import Student
from models.attendance import Attendance

student_attendance_bp=Blueprint("student_attendance_bp",__name__,url_prefix="/student/operation/attendance")
@student_attendance_bp.route("/my",methods=["GET"])
@jwt_required()
def my_attendance():
    claims=get_jwt()
    if claims.get("role")!="student":
        return jsonify({
            "success": False,
            "message": "Student access only"
        }), 403

    current_student_id=int(get_jwt_identity())
    student=Student.query.filter_by(
        id=current_student_id
    ).first()
    
    if not student:
        return jsonify({
            "success":False,
            "message":"Student not found"
        }),400
    attendance_records = Attendance.query.filter_by(
        student_id=student.id
    ).all()

    attendance_list = []

    for attendance in attendance_records:
        attendance_list.append(attendance.to_dict())

    total_attendance = len(attendance_records)

    present_count = Attendance.query.filter_by(
        student_id=student.id,
        status="Present"
    ).count()

    absent_count = Attendance.query.filter_by(
        student_id=student.id,
        status="Absent"
    ).count()

    late_count = Attendance.query.filter_by(
        student_id=student.id,
        status="Late"
    ).count()

    attendance_percentage = 0

    if total_attendance > 0:
        attendance_percentage = round((present_count / total_attendance) * 100, 2)
  
    return jsonify({
        "success": True,
        "message": "Attendance fetched successfully",
        "summary": {
            "total_attendance": total_attendance,
            "present": present_count,
            "absent": absent_count,
            "late": late_count,
            "attendance_percentage": attendance_percentage
        },
        "attendance": attendance_list
    }), 200    