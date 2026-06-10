from flask import Blueprint, jsonify, request

from dbms.db import db
from models.institute import Institution
from models.faq import Faq
from models.leads import Lead
from models.chat import ChatHistory
from utils.open_router import generate_admission_reply

admission_bot_bp=Blueprint("admission_bot_bp",__name__,url_prefix="/admission-bot")
@admission_bot_bp.route("/chat/<int:institution_id>",methods=["POST"])

def admission_chat(institution_id):
    institute=Institution.query.filter_by(
        id=institution_id
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

    user_message = data.get("message")
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")
    course_interest = data.get("course_interest")

    if not user_message:
        return jsonify({
            "success": False,
            "message": "Message is required"
        }), 400   
    faqs=Faq.query.filter_by(
        institution_id=institute.id
    ).all()
    faq_context = ""

    for faq in faqs:
        faq_context += f"Q: {faq.question}\n"
        faq_context += f"A: {faq.answer}\n"
        faq_context += f"Category: {faq.category}\n\n"
    has_contact = bool(name and phone)
    bot_reply=generate_admission_reply(
        user_message=user_message,
        faq_context=faq_context,
        has_contact=has_contact
    )
    
    lead_created = False
    lead_id=None

    try:
        
        if name and phone:
            existing_lead = Lead.query.filter_by(
                institution_id=institute.id,
                phone=phone
            ).first()

            if existing_lead:
                existing_lead.name = name
                existing_lead.email = email or existing_lead.email
                existing_lead.course_interest = course_interest or existing_lead.course_interest
                existing_lead.message = user_message
                existing_lead.source = "AI Bot"

                lead_id = existing_lead.id
                lead_created = False

            else:
                lead = Lead(
                    institution_id=institute.id,
                    name=name,
                    phone=phone,
                    email=email,
                    course_interest=course_interest,
                    message=user_message,
                    source="AI Bot",
                    status="New"
                )

                db.session.add(lead)
                db.session.flush()
                lead_created=True
                lead_id=lead.id
        chat=ChatHistory(
                    institution_id=institution_id,
                    lead_id=lead_id,
                    sender="visitor",
                    message=user_message,
                    response=bot_reply
                )
        db.session.add(chat)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "AI response generated successfully",
            "reply": bot_reply,
            "lead_created": lead_created,
            "lead_id": lead_id
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Admission Bot Error:", e)

        return jsonify({
            "success": False,
            "message": "Something went wrong while processing admission chat"
        }), 500

               