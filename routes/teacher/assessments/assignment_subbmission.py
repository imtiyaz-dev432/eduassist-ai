from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models.institute import Institution
from models.assignment import Assignment
from models.assignment_submission import AssignmentSubmission
from dbms.db import db

teacher_submission_check_bp=Blueprint("teacher_submission_check_bp",__name__,url_prefix="/teacher/assessments/assignment")
@teacher_submission_check_bp.route("/fetch/<int:assignment_id>",methods=["GET"])
@jwt_required()
def teacherr_check(assignment_id):
    current_user_id=int(get_jwt_identity())
    assignment = Assignment.query.filter_by(
        id=assignment_id
    ).first()

    if not assignment:
        return jsonify({
            "success": False,
            "message": "Assignment not found"
        }), 404

    institution = Institution.query.filter_by(
        id=assignment.institution_id,
        user_id=current_user_id
    ).first()

    if not institution:
        return jsonify({
            "success": False,
            "message": "Unauthorized to view submissions for this assignment"
        }), 403

    submissions = AssignmentSubmission.query.filter_by(
        assignment_id=assignment.id
    ).all()

    submission_list = []

    for submission in submissions:
        submission_list.append(submission.to_dict())

    return jsonify({
        "success": True,
        "message": "Assignment submissions fetched successfully",
        "submissions": submission_list
    }), 200

@teacher_submission_check_bp.route("/check/<int:assignment_submission_id>",methods=["PATCH"])
@jwt_required()
def check_assignment(assignment_submission_id):
    current_user_id=int(get_jwt_identity())
    assignment_submission=AssignmentSubmission.query.filter_by(
        id=assignment_submission_id
    ) .first()

    if not assignment_submission:
        return  jsonify({
            "success":False,
            "message":"Assignment submission not found"
        }),400
    assignment=Assignment.query.filter_by(
        id=assignment_submission.assignment_id
    ).first()

    if not assignment:
        return jsonify({
            "success":False,
            "message":"Assignment not found"
        }),404
    institute=Institution.query.filter_by(
      user_id=current_user_id,
      id=assignment_submission.institution_id        
    ).first()

    if not institute:
        return jsonify({
            "success":False,
            "message":"Unauthorized to  update assignment"
        }),403

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    marks = data.get("marks")
    feedback = data.get("feedback")
    status = data.get("status", "Checked")

    assignment_submission.marks = marks
    assignment_submission.feedback = feedback
    assignment_submission.status = status
    assignment_submission.checked_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Submission checked successfully",
        "submission": assignment_submission.to_dict()
    }), 200    

