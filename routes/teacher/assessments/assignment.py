from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime 
from dbms.db import db

from models.institute import Institution
from models.batch import Batch
from models.assignment import Assignment

assignment_bp=Blueprint("assignment_bp",__name__,url_prefix="/assignment")
@assignment_bp.route("/add/<int:batch_id>",methods=['POST'])
@jwt_required()
def add_assignment(batch_id):
    current_user_id=int(get_jwt_identity())
    batch=Batch.query.filter_by(
        id=batch_id
    ).first()

    if not batch:
        return jsonify({
            "success":False,
            "message":"Batch not found"
        }),404

    institute=Institution.query.filter_by(
        id=batch.institution_id,
        user_id=current_user_id
    ).first()

    if not institute:
        return jsonify({
            "success":False,
            "message":"Institute not found"
        }),404

    data=request.get_json()
    if not data:
        return jsonify({
            "success":False,
            "message":"Request body is required"
        })    ,400

    title=data.get("title")
    description=data.get("description")
    due_date=data.get("due_date")
    max_marks=data.get("max_marks")
    status=data.get("status","Active")
    if not title:
        return jsonify({
            "success":False,
           "message":"Title is required"}),400

    due_date_obj=None
    if due_date:
        due_date_obj=datetime.strptime(
            due_date,
            "%Y-%m-%d"
        ).date()

    new_assignment = Assignment(
        institution_id=batch.institution_id,
        course_id=batch.course_id,
        batch_id=batch.id,
        title=title,
        description=description,
        due_date=due_date_obj,
        max_marks=max_marks,
        status=status
    )

    db.session.add(new_assignment)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Assignment created successfully",
        "assignment": new_assignment.to_dict()
    }), 201               

#get
@assignment_bp.route("/get/<int:batch_id>",methods=["GET"])
@jwt_required()
def get_assignment(batch_id):
    current_user_id=int(get_jwt_identity())
    batch=Batch.query.filter_by(
        id=batch_id
    ).first()

    if not batch:
        return jsonify({
            "success":False,
            "message":"Batch not found"
        }),404

    institute=Institution.query.filter_by(
        id=batch.institution_id,
        user_id=current_user_id
    )    .first()

    if not institute:
        return jsonify({
            "success":False,
            "message":"Unauthorized to view assignments for this batch"
        }),403

    assignments=Assignment.query.filter_by(batch_id=batch_id).all()
    assignment_list=[]
    for assignment in assignments:
        assignment_list.append(assignment.to_dict())

    return jsonify({
        "success":True,
        "message":"Data fetched successfully",
        "assignment_list":assignment_list
    })  ,200  

#update
@assignment_bp.route("/update/<int:assignment_id>",methods=["PATCH"])
@jwt_required()
def update_assignment(assignment_id):
    current_user_id=int(get_jwt_identity())
    assignment=Assignment.query.filter_by(
        id=assignment_id
    ).first()

    if not assignment:
        return jsonify({
            "success":False,
            "message":"Assignment not found"}),404
    institute=Institution.query.filter_by(
        id=assignment.institution_id,
        user_id=current_user_id
    ).first()

    if not institute:
        return jsonify({
            "success":False,
            "message":"Unauthorized to update assignment"
        }),403

    data=request.get_json()
    if not data:
        return jsonify({
            "success":False,
            "message":"Request body is required"
        }),400
    title=data.get("title",assignment.title)
    description=data.get("description",assignment.description)
    due_date=data.get("due_date")
    max_marks=data.get("max_marks",assignment.max_marks)
    status=data.get("status",assignment.status)
    allowed_status = ["Active", "Closed", "Draft"]
    if status not in allowed_status:
       return jsonify({
        "success": False,
        "message": "Invalid assignment status"
    }), 400
    assignment.title = title
    assignment.description = description
    assignment.max_marks = max_marks
    assignment.status = status
    if due_date:
        assignment.due_date=datetime.strptime(
            due_date,
            "%Y-%m-%d"
        ).date()

    
    db.session.commit()

    return jsonify({
    "success": True,
    "message": "Assignment updated successfully",
    "assignment": assignment.to_dict()
}), 200    

#delete
@assignment_bp.route("/delete/<int:assignment_id>",methods=["DELETE"])
@jwt_required()
def delete_assignment(assignment_id):
    current_user_id=int(get_jwt_identity())
    assignment=Assignment.query.filter_by(
        id=assignment_id
    ).first()

    if not assignment:
        return jsonify({
            "success":False,
            "message":"Assignment not found"
        }),404

    institute=Institution.query.filter_by(
        id=assignment.institution_id,
        user_id=current_user_id
    ).first()

    if not institute:
        return jsonify({
            "success":False,
            "message":"Unauthorized to delete ths assignment"
                    }),403

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({
        "success":True,
        "message":"Assignment deleted successfully"
    }),200