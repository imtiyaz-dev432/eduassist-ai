from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from dbms.db import db
from models.institute import Institution
from models.assignment import Assignment
from models.assignment_submission import AssignmentSubmission
from models.student import Student


assignment_submission_bp = Blueprint(
    "assignment_submission_bp",
    __name__,
    url_prefix="/assignment_submission"
)


@assignment_submission_bp.route("/add/<int:assignment_id>/<int:student_id>", methods=["POST"])
@jwt_required()
def add_submission(assignment_id, student_id):
    current_user_id = int(get_jwt_identity())

    assignment = Assignment.query.filter_by(id=assignment_id).first()

    if not assignment:
        return jsonify({
            "success": False,
            "message": "Assignment not found"
        }), 404

    institute = Institution.query.filter_by(
        id=assignment.institution_id,
        user_id=current_user_id
    ).first()

    if not institute:
        return jsonify({
            "success": False,
            "message": "Unauthorized to submit assignment"
        }), 403

    student = Student.query.filter_by(id=student_id).first()

    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    if student.batch_id != assignment.batch_id:
        return jsonify({
            "success": False,
            "message": "Student does not belong to this assignment batch"
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    answer_text = data.get("answer_text")
    file_url = data.get("file_url")

    if not answer_text and not file_url:
        return jsonify({
            "success": False,
            "message": "Answer text or file URL is required"
        }), 400

    existing_submission = AssignmentSubmission.query.filter_by(
        assignment_id=assignment.id,
        student_id=student.id
    ).first()

    if existing_submission:
        return jsonify({
            "success": False,
            "message": "Assignment already submitted by this student"
        }), 409

    submission_status = "Submitted"

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

#get
@assignment_submission_bp.route("/get/<int:assignment_id>/<int:student_id>", methods=["GET"])
@jwt_required()
def get_assignment_submission(assignment_id, student_id):
    current_user_id = int(get_jwt_identity())

    assignment = Assignment.query.filter_by(id=assignment_id).first()

    if not assignment:
        return jsonify({
            "success": False,
            "message": "Assignment not found"
        }), 404

    institute = Institution.query.filter_by(
        id=assignment.institution_id,
        user_id=current_user_id
    ).first()

    if not institute:
        return jsonify({
            "success": False,
            "message": "Unauthorized to get assignment submission"
        }), 403

    student = Student.query.filter_by(id=student_id).first()

    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    if student.batch_id != assignment.batch_id:
        return jsonify({
            "success": False,
            "message": "Student does not belong to this assignment batch"
        }), 400

    assignment_submissions = AssignmentSubmission.query.filter_by(
        student_id=student_id,
        assignment_id=assignment_id
    ).all()

    assignment_submission_list = []

    for submission in assignment_submissions:
        assignment_submission_list.append(submission.to_dict())

    return jsonify({
        "success": True,
        "message": "Assignment submissions fetched successfully",
        "assignment_submission_list": assignment_submission_list
    }), 200


# Teacher/owner route: marks, feedback, review status
@assignment_submission_bp.route("/check/<int:assignment_submission_id>", methods=["PATCH"])
@jwt_required()
def check_assignment_submission(assignment_submission_id):
    current_user_id = int(get_jwt_identity())

    assignment_submission = AssignmentSubmission.query.filter_by(
        id=assignment_submission_id
    ).first()

    if not assignment_submission:
        return jsonify({
            "success": False,
            "message": "Assignment submission not found"
        }), 404

    assignment = Assignment.query.filter_by(
        id=assignment_submission.assignment_id
    ).first()

    if not assignment:
        return jsonify({
            "success": False,
            "message": "Assignment not found"
        }), 404

    student = Student.query.filter_by(
        id=assignment_submission.student_id
    ).first()

    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    institute = Institution.query.filter_by(
        id=assignment_submission.institution_id,
        user_id=current_user_id
    ).first()

    if not institute:
        return jsonify({
            "success": False,
            "message": "Unauthorized to check this submission"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    marks = data.get("marks", assignment_submission.marks)
    feedback = data.get("feedback", assignment_submission.feedback)
    status = data.get("status", assignment_submission.status)

    allowed_status = [
        "Submitted",
        "Late",
        "Under Review",
        "Checked",
        "Rejected"
    ]

    if status not in allowed_status:
        return jsonify({
            "success": False,
            "message": "Invalid submission status"
        }), 400

    assignment_submission.marks = marks
    assignment_submission.feedback = feedback
    assignment_submission.status = status

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Assignment submission checked successfully",
        "submission": assignment_submission.to_dict()
    }), 200


# Student edit route: answer/file edit before deadline and before review
@assignment_submission_bp.route("/edit/<int:assignment_submission_id>", methods=["PATCH"])
@jwt_required()
def edit_assignment_submission(assignment_submission_id):
    current_user_id = int(get_jwt_identity())

    assignment_submission = AssignmentSubmission.query.filter_by(
        id=assignment_submission_id
    ).first()

    if not assignment_submission:
        return jsonify({
            "success": False,
            "message": "Assignment submission not found"
        }), 404

    assignment = Assignment.query.filter_by(
        id=assignment_submission.assignment_id
    ).first()

    if not assignment:
        return jsonify({
            "success": False,
            "message": "Assignment not found"
        }), 404

    student = Student.query.filter_by(
        id=assignment_submission.student_id
    ).first()

    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    institute = Institution.query.filter_by(
        id=assignment_submission.institution_id,
        user_id=current_user_id
    ).first()

    if not institute:
        return jsonify({
            "success": False,
            "message": "Unauthorized to edit this submission"
        }), 403

    if student.batch_id != assignment.batch_id:
        return jsonify({
            "success": False,
            "message": "Student does not belong to this assignment batch"
        }), 400

    if assignment_submission.status in ["Under Review", "Checked", "Rejected"]:
        return jsonify({
            "success": False,
            "message": "Submission is locked because teacher has started or completed review"
        }), 400

    if assignment.due_date and datetime.utcnow().date() > assignment.due_date:
        return jsonify({
            "success": False,
            "message": "Deadline has passed. Submission cannot be edited"
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    answer_text = data.get("answer_text", assignment_submission.answer_text)
    file_url = data.get("file_url", assignment_submission.file_url)

    if not answer_text and not file_url:
        return jsonify({
            "success": False,
            "message": "Answer text or file URL is required"
        }), 400

    assignment_submission.answer_text = answer_text
    assignment_submission.file_url = file_url

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Assignment submission edited successfully",
        "submission": assignment_submission.to_dict()
    }), 200


@assignment_submission_bp.route("/delete/<int:assignment_submission_id>", methods=["DELETE"])
@jwt_required()
def delete_assignment_submission(assignment_submission_id):
    current_user_id = int(get_jwt_identity())

    assignment_submission = AssignmentSubmission.query.filter_by(
        id=assignment_submission_id
    ).first()

    if not assignment_submission:
        return jsonify({
            "success": False,
            "message": "Assignment submission not found"
        }), 404

    assignment = Assignment.query.filter_by(
        id=assignment_submission.assignment_id
    ).first()

    if not assignment:
        return jsonify({
            "success": False,
            "message": "Assignment not found"
        }), 404

    student = Student.query.filter_by(
        id=assignment_submission.student_id
    ).first()

    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    institute = Institution.query.filter_by(
        id=assignment_submission.institution_id,
        user_id=current_user_id
    ).first()

    if not institute:
        return jsonify({
            "success": False,
            "message": "Unauthorized to delete this submission"
        }), 403

    if student.batch_id != assignment.batch_id:
        return jsonify({
            "success": False,
            "message": "Student does not belong to this assignment batch"
        }), 400

    db.session.delete(assignment_submission)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Assignment submission deleted successfully"
    }), 200