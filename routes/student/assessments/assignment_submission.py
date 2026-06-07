from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

from dbms.db import db
from models.assignment import Assignment
from models.assignment_submission import AssignmentSubmission
from models.student import Student

student_assignment_submission_bp=Blueprint("assignment_submission_bp",__name__,url_prefix="/student/assessments/assignment_submission")
@student_assignment_submission_bp.route("/submit/<int:assignment_id>",methods=["POST"])
@jwt_required()
def submit_assignment(assignment_id):
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
    assignment=Assignment.query.filter_by(
        id=assignment_id
    ).first()

    if not assignment:
        return jsonify({
            "success":False,
            "message":"Assignment not found"
        }),404

    if assignment.batch_id!=student.batch_id:
        return jsonify({
            "success":False,
            "message":"Unauthorized to submit this assignment"
        })   ,403
    data=request.get_json()
    if not data:
        return jsonify({
            "succeess":False,
            "message":"Request body is required"
        })   ,400

    answer_text=data.get("answer_text")
    file_url=data.get("file_url")
    if not file_url and not answer_text:
        return jsonify({
            "success":False,
            "message": "Answer text or file URL is required"
        })   ,400

    existing_submission=AssignmentSubmission.query.filter_by(
        student_id=student.id,
        assignment_id=assignment.id
    ).first()
    if existing_submission:
        return jsonify({
            "success":False,
            "message":"Assignment is already submitted"
        })  ,409

    submission_status="Submitted"

    if assignment.due_date and datetime.utcnow().date() > assignment.due_date:
        submission_status = "Late"

    new_submission = AssignmentSubmission(
        assignment_id=assignment.id,
        institution_id=assignment.institution_id,
        course_id=assignment.course_id,
        batch_id=assignment.batch_id,
        student_id=student.id,
        answer_text=answer_text,
        file_url=file_url,
        status=submission_status
    )

    db.session.add(new_submission)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Assignment submitted successfully",
        "submission": new_submission.to_dict()
    }), 201    