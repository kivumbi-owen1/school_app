from school_app import db, login_manager
from datetime import datetime
import pytz
from sqlalchemy import func
from flask_login import UserMixin
from flask import redirect, url_for, flash

# Set timezone
AFRICA_KAMPALA_TZ = pytz.timezone('Africa/Kampala')

@login_manager.user_loader
def load_user(user_id):
    try:
        user_type, real_id = user_id.split('-', 1)
        if user_type == 'student':
            return Student.query.get(int(real_id))
        elif user_type == 'admin':
            return Admin.query.get(int(real_id))
    except Exception:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    flash('Please login to access this page', 'danger')
    return redirect(url_for('auth.student_login'))

class Student(db.Model, UserMixin):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    student_names = db.Column(db.String(150), nullable=False)
    student_registration_number = db.Column(db.String(150), nullable=False)
    program = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year_of_study = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    enrollment_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(AFRICA_KAMPALA_TZ))

    complaints = db.relationship('Complaint', backref='complaint_student', lazy=True)

    def get_id(self):
        return f"student-{self.student_id}"

    def __repr__(self):
        return f"<Student {self.student_names} ({self.student_registration_number})>"

class Complaint(db.Model):
    __tablename__ = 'complaints'

    complaint_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    course_name = db.Column(db.String(120), nullable=False)
    course_code = db.Column(db.String(120), nullable=False)
    course_intake = db.Column(db.String(120), nullable=False)
    complaint_text = db.Column(db.Text, nullable=False)
    lecturer_names = db.Column(db.String(120), nullable=False)
    lecturer_email = db.Column(db.String(120), nullable=False)
    date_filed = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Complaint ID: {self.complaint_id}>"

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(AFRICA_KAMPALA_TZ))

    def get_id(self):
        return f"admin-{self.admin_id}"

    def __repr__(self):
        return f"<Admin {self.email}>"
