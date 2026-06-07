from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

from dbms.db import db
from models.assignment import Assignment
from models.assignment_submission import AssignmentSubmission
from models.student import Student

student_assignment_bp=Blueprint("student_assignment_bp",__name__,url_prefix="/student/assessments/assignment")
@student_assignment_bp.route("/my",methods=["GET"])
@jwt_required()
def student_assignment():
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
    assignments=Assignment.query.filter_by(
        batch_id=student.batch_id,
        status="Active"
    ).all()
    assignment_list=[]
    for assignment in assignments:
        submission = AssignmentSubmission.query.filter_by(
            assignment_id=assignment.id,
            student_id=student.id
        ).first()

        assignment_list.append({
            "id": assignment.id,
            "institution_id": assignment.institution_id,
            "course_id": assignment.course_id,
            "batch_id": assignment.batch_id,
            "title": assignment.title,
            "description": assignment.description,
            "file_url": assignment.file_url,
            "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
            "max_marks": assignment.max_marks,
            "status": assignment.status,
            "created_at": assignment.created_at.isoformat() if assignment.created_at else None,

            "is_submitted": True if submission else False,
            "submission_id": submission.id if submission else None,
            "submission_status": submission.status if submission else None,
            "marks_obtained": submission.marks if submission else None,
            "teacher_feedback": submission.feedback if submission else None
        })

    return jsonify({
        "success": True,
        "message": "Assignments fetched successfully",
        "assignments": assignment_list
    }), 200 
