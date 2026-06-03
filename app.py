from flask import Flask,jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from dbms.db import db
from flask_migrate import Migrate
from block import BLOCKLIST
#models
from models.user import User
from models.institute import Institution
from models.course import Course
from models.batch import Batch
from models.student import Student
from models.fee import Fee
from models.payment import Payment
from models.attendance import Attendance
from models.fee_reminder import FeeReminder
from models.assignment import Assignment
from models.assignment_submission import AssignmentSubmission
from models.quize import Quiz
from models.quiz_question import QuizQuestion
from models.faq import Faq
from models.leads import Lead
from models.chat import ChatHistory
from models.quizsubmission import QuizSubmission
from models.quiz_submission_answer import QuizSubmissionAnswer
#route
from routes.auth import auth_bp
from routes.otp import otp_bp
from routes.teacher.institution import institute_bp
from routes.teacher.academics.course import course_bp
from routes.teacher.academics.batch import batch_bp
from routes.teacher.academics.student import teacher_student_bp
from routes.teacher.finance.fee import fee_bp
from routes.teacher.finance.payment import payment_bp
from routes.teacher.operations.attendance import attendance_bp
from routes.teacher.finance.fee_reminder import fee_reminder_bp
from routes.teacher.assessments.assignment import assignment_bp
from routes.teacher.assessments.assignment_subbmission import assignment_submission_bp
from routes.teacher.assessments.quize import quiz_bp
from routes.teacher.assessments.quiz_question import quiz_question_bp
from routes.student_auth import student_auth_bp

app=Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
migrate=Migrate(app,db)
jwt=JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header,jwt_payload):
    return jwt_payload.get('jti') in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token_loader(jwt_header,jwt_payload):
      return ({
        "description":"user has been logged out",
        "error":"token-revoked"
      },401)

#register blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(otp_bp)
app.register_blueprint(institute_bp)
app.register_blueprint(course_bp)
app.register_blueprint(batch_bp)
app.register_blueprint(teacher_student_bp)
app.register_blueprint(fee_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(fee_reminder_bp)
app.register_blueprint(assignment_bp)
app.register_blueprint(assignment_submission_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(quiz_question_bp)
app.register_blueprint(student_auth_bp)
@app.route("/",methods=["GET"])
def home():
    return jsonify({
        "message":"eduassist ai is running successfully"
    }),200

if __name__ == "__main__":
    app.run(debug=True)